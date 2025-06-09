from django.contrib import admin
from .models import Order, OrderItem, Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    fields = ['creator', 'name','detailed_address','city','district','email','tel']
admin.site.register(Address, AddressAdmin)

admin.site.register(Order)
admin.site.register(OrderItem)
