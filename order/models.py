from django.db import models
import uuid



# Create your models here.
class Address(models.Model):
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.TextField(null=False, blank=True) 
    detailed_address = models.TextField(null=False, blank=True) 
    city = models.TextField(null=True, blank=True) 
    district = models.TextField(null=True, blank=True) 
    email = models.EmailField(unique=True, null=True, blank=True)
    tel = models.TextField(null=False, blank=False) 
    is_default = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Address {self.detailed_address} with belongs to email {self.email} and tel {self.tel} created by {self.creator.email}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    ORDER_PAYMENT_CHOICES = [
        ('COD', 'Cash On Delivery'),
        ('BANK', 'Bank Transfer')
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_address = models.ForeignKey('Address', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    is_paid = models.BooleanField(null=False, default=False)
    payment = models.CharField(max_length=50, choices=ORDER_PAYMENT_CHOICES, default='COD')
    total_quantity = models.IntegerField(default=0, null=False, blank=False)
    total_amount = models.IntegerField(default=0, null=False, blank=False)
    tax = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    bank_proof = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return f"Order #{self.uuid} by {self.order_address.email}-{self.order_address.tel}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.unit_price
    
