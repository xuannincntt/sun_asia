from django.shortcuts import render
from accounts.models import User
from .models import Address, Order, OrderItem
from django.utils.timezone import now

# Create your views here.
def create_order(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    address = Address.objects.get(user=user_id) if user_id else {
        'address': user.address if user else ''
    }
    if request.method == "POST":
        return render(request, 'order/order_success.html')
    return render(request, 'order/order.html', {'timestamp': now().timestamp(), 'user': user, 'address': address })

def get_order_detail(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'order/order_detail.html', {'timestamp': now().timestamp(), 'user': user})
