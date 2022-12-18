from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [  
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('checkout/', views.orderproduct, name='orderproduct'),
    path('createorderrazorpay/',views.Create_RazorPayOrder),
    path('createorderrazorpaycod/',views.Create_RazorPayOrder_Cod),
]