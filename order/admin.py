from django.contrib import admin
from .models import Order, OrderItem, Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    fields = ['creator', 'name','detailed_address','city','district','email','tel','ward']
admin.site.register(Address, AddressAdmin)

admin.site.register(Order)

class OrderItemAdmin(admin.ModelAdmin):
    fields = ['order', 'product','quantity','city','price','subtotal']
admin.site.register(OrderItem, OrderItemAdmin)
