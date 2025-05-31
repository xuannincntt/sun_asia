from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from django.http import HttpResponse
from django.utils.timezone import now

def home(request):
    response = render(request, 'home.html')
    response.set_cookie('user_id',1)
    return response


def cart(request):
    user_id = request.COOKIES.get('user_id', 0)
    cart = request.COOKIES.get('cart', [])
    return render(request, 'cart.html', {'timestamp': now().timestamp()})