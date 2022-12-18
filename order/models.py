from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Variants
from django.forms import ModelForm
# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    PAYMENT_METHOD = (
        ('Semi Cash On Delivery', 'Semi Cash On Delivery'),
        ('RazorPay', 'RazorPay'),

    )
    full_name = models.CharField(max_length=500, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE)
    code = models.CharField(max_length=5, editable=False )
    phone = models.CharField(blank=True, max_length=10)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    pincode = models.CharField(blank=True, max_length=6)
    total = models.FloatField()
    payment_method = models.CharField(default='Cash On Delivery', max_length=30,choices=PAYMENT_METHOD )
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['full_name','address','phone','city','state','pincode', 'payment_method']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title