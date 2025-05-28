from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation

def home(request):
    return render(request, 'home.html')