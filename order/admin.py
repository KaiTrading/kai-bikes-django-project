from django.contrib import admin
from order.models import OrderProduct, ShopCart, Order
# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity' ]
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product','price','quantity','amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','total','status']
    list_filter = ['status']
    readonly_fields = ('address','city','state','pincode','phone','full_name','ip','phone','city','total')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product','price','quantity','amount']
    list_filter = ['product']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)