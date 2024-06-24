"""
URL configuration for pet_store_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from petapp.views import petview, petdetail
from django.conf import settings
from django.conf.urls.static import static
from petapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('petview/', petview.as_view()),
    path('filter/', views.filterpetview, name='filterbycategory'),
    path('sort/', views.sortpetview, name='sortby'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('details/<int:pk>/', petdetail.as_view(), name='detail'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('changequantity/', views.changequantity, name='cq'),
    path('summary/', views.summary, name='summary'),
    path('payment/', views.payment, name='payment'),
    path('paymentsuccess', views.paymentsuccess, name='paymentsuccess'),
    path('logout', views.logout, name='logout'),
    path('petdetail/<slug:slug>',petdetail.as_view(),name='petdetail'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
