from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import pet, Customer1, cart, Order, Payment, Orderdetail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
import razorpay
from pet_store_project import settings

# Create your views here.
class petview(ListView):
    model = pet
    template_name = 'petview.html'
    context_object_name = 'petobject'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context  

    
def filterpetview(request):
    # species = request.POST.get('species')
    petdetails = pet.cpetobj.filterdata('Corgi')
    return render(request,'petview.html',{'petobject':petdetails}) 

def sortpetview(request):
    petdetails = pet.cpetobj.sortdata()
    return render(request,'petview.html',{'petobject':petdetails}) 

def search(request):
    if request.method == "POST":
        session = request.session['sessionvalue'] # in function based view this is valid
        searchdata = request.POST.get('searchquery')
        print(searchdata)
        petobject = pet.objects.filter(Q(name__icontains =searchdata)|Q(breed__icontains=searchdata))
        print(petobject)
        return render(request, 'petview.html', {'petobject': petobject, 'session':session}) 
    
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        epassword = make_password(password)
        custobject = Customer1(name=name, contact=contact, email=email, password=epassword)
        print(custobject)
        custobject.save()
        return redirect('../login/')
        
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('user')        
        password = request.POST.get('pass')
        # print('username',username)
        # print('password',password)
        cust = Customer1.objects.filter(email = username)
        print('cust: ', cust)

        if cust:
            custobject1 = Customer1.objects.get(email = username)
            print('custobject1: ', custobject1)
            flag = check_password(password, custobject1.password)
            print('flag: ', flag)
            if flag: 
                # request.session['sessionvalue'] = custobject1.email
                request.session['sessionvalue'] = custobject1.email
                return redirect('../petview/')
            else:
                return render(request, 'login.html', {'message':'Incorrect username or password'})
        else:
            return render(request, 'login.html', {'message':'Incorrect username or password'})


class petdetail(DetailView):
    model = pet
    template_name = 'details.html'
    context_object_name = 'i'
    
    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

def addtocart(request):
    productid = request.POST.get("productid")
    custsession = request.session['sessionvalue']  # email of customer
    custobj = Customer1.objects.get(email = custsession) #fetch record from database table using email from session
    pobj = pet.objects.get(id = productid)

    flag = cart.objects.filter(cid = custobj.id, pid = pobj.id)
    if flag:
        cartobj = cart.objects.get(cid = custobj.id, pid = pobj.id)
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = pobj.price * cartobj.quantity
        cartobj.save()
    else:
        cartobj = cart(cid = custobj, pid = pobj, quantity = 1, totalamount = pobj.price*1 )
        cartobj.save()

    return redirect('../petview/')

def viewcart(request):
    custsession = request.session['sessionvalue']  # email of customer
    print('custsession', custsession)
    custobj = Customer1.objects.get(email = custsession)
    cartobj = cart.objects.filter(cid = custobj.id)

    return render(request, 'cart.html', {'cartobj': cartobj, 'session':custsession})

def changequantity(request):
    customer_email = request.session['sessionvalue']
    pid = request.POST.get('pid')
    custobj = Customer1.objects.get(email = customer_email)
    pobj = pet.objects.get(id = pid)
    cartobj = cart.objects.get(cid = custobj.id, pid = pobj.id)

    if request.POST.get('changequantity') == '+':
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = cartobj.quantity * pobj.price
        cartobj.save()
    
    elif request.POST.get('changequantity') == '-':
        if cartobj.quantity == 1:
            cartobj.delete()
        else:
            cartobj.quantity = cartobj.quantity - 1
            cartobj.totalamount = cartobj.quantity * pobj.price
            cartobj.save()

    return redirect('../viewcart/')

def summary(request):
    custsession = request.session['sessionvalue'] 
    custobj = Customer1.objects.get(email = custsession)
    cartobj = cart.objects.filter(cid = custobj.id)

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1
    
    return render(request, 'summary.html' , {'session': custsession, 'totalbill': totalbill, 'cartobj': cartobj, 'count': count})

def payment(request):
    firstname = request.POST.get('fn')
    lastname = request.POST.get('ln')
    address = request.POST.get('address')
    state = request.POST.get('state')
    city = request.POST.get('city')
    pincode = request.POST.get('pin')
    phonenumber = request.POST.get('phone')
    datevar = date.today()
    orderobj = Order(firstname=firstname, lastname=lastname, address = address, state=state, city=city, pincode=pincode, phonenumber=phonenumber, orderdate=datevar, orderstatus = 'pending')
    orderobj.save()

    orderno = str(orderobj.id)+str(datevar).replace('-','')
    orderobj.ordernumber = orderno
    orderobj.save()
    print('orderobj: ', orderobj) 

    custsession = request.session['sessionvalue'] 
    print('custsession: ', custsession)
    custobj = Customer1.objects.get(email = custsession)
    cartobj = cart.objects.filter(cid = custobj.id)
    print('cartobj: ', cartobj)

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
            
    from django.core.mail import EmailMessage
    sm = EmailMessage('Order placed', 'Your order from the pet store app has been placed, total bill is '+str(totalbill), to=['samruddhiaware@gmail.com'])
    sm.send()

    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 

    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '../PetView'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print("context: ", context)

    return render(request, 'payment.html', {'orderobj': orderobj, 'session': custsession, 'cartobj': cartobj, 'totalbill': totalbill, 'context':context})

def paymentsuccess(request):
    orderno = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    print('orderid: ', orderno)
    print('tid: ', tid)
    custsession = request.session['sessionvalue'] 
    print('custsession: ', custsession)
    custobj = Customer1.objects.get(email = custsession)
    print('custobj: ', custobj)
    cartobj = cart.objects.filter(cid = custobj.id)
    print('cartobj: ', cartobj)
    orderobj = Order.objects.get(ordernumber = orderno)
    print('orderobj: ', orderobj)   

    paymentobj = Payment(customerid = custobj, orderid = orderobj, paymentmode = 'paypal', paymentstatus='paid', transactionid = tid)
    paymentobj.save() 
    print('paymentobj: ', paymentobj)

    for i in cartobj:
        orderdetailobj = Orderdetail(ordernumber = orderno, customerid=custobj, productid=i.pid,  quantity=i.quantity, totalprice=i.totalamount,  paymentid=paymentobj)
        orderdetailobj.save()  
        print('orderdetailobj: ', orderdetailobj)
        i.delete()

    return render(request, 'paymentsuccess.html', {'orderdetailobj': orderdetailobj, 'paymentobj': paymentobj, 'session': custsession})

def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../login/')






    

