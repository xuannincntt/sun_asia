from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from accounts.models import User
from django.utils.timezone import now

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