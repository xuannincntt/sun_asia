from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from accounts.models import User
from order.models import Address, Order, OrderItem
from django.utils.timezone import now
from django.views.decorators.cache import never_cache

def home(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'home.html', {'user': user})

def logout_view(request):
    del request.session['user_id']
    return redirect('/')

def cart(request):
    cart = request.COOKIES.get('cart', [])
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'cart.html', {'timestamp': now().timestamp(), 'user': user})

@never_cache
def checkout(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    try:
        default_address = Address.objects.get(creator=user_id)
    except:
        default_address = {
            'address': user.fixed_address if user.fixed_address else ''
        }
    if request.method == "POST":
        return render(request, 'order/order_success.html')
    return render(request, 'checkout.html', {'timestamp': now().timestamp(), 'user': user, 'default_address': default_address })