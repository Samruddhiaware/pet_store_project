from django.db import models
from django.db.models import Manager 

# Create your models here.

class Custommanager(models.Manager):
    def sortdata(self):
        return super().get_queryset().order_by('price')
    
    def filterdata(self, a):
        return super().get_queryset().filter(species=a)

class pet(models.Model):    
    name=models.CharField(max_length=200)
    gender=(("Male","male"),("Female","female"))
    image=models.ImageField(upload_to="media")
    species=models.CharField(max_length=200)
    breed=models.CharField(max_length=200)
    age=models.IntegerField()
    gender=models.CharField(max_length=200,choices=gender)
    description=models.CharField(max_length=200)
    price=models.FloatField()
    slug = models.SlugField(default='',null=False)

    cpetobj = Custommanager()
    objects = Manager()

    class Meta:
        db_table="pet"

class Customer1(models.Model):
    name=models.CharField(max_length=30)
    contact = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=200)

    class Meta:
        db_table='customer1'

class cart(models.Model):
    cid = models.ForeignKey(Customer1, on_delete=models.CASCADE)
    pid = models.ForeignKey(pet, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalamount = models.FloatField()

    class Meta:
        db_table='cart'

class Order(models.Model):
    ordernumber = models.CharField(max_length=100)
    orderdate = models.DateField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phonenumber = models.BigIntegerField()
    pincode = models.BigIntegerField()
    orderstatus = models.CharField(max_length=50)

    class Meta:
        db_table = 'order'

class Payment(models.Model):
    customerid = models.ForeignKey(Customer1, on_delete=models.CASCADE)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    paymentmode = models.CharField(max_length=100, default='paypal')
    paymentstatus = models.CharField(max_length=100, default='pending')
    transactionid = models.CharField(max_length=200)    

    class Meta:
        db_table = 'payment'

class Orderdetail(models.Model):    
    ordernumber = models.CharField(max_length=100)
    customerid = models.ForeignKey(Customer1, on_delete=models.CASCADE)
    productid = models.ForeignKey(pet, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalprice = models.IntegerField()
    paymentid = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'orderdetail'