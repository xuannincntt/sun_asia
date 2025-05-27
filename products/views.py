from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, '/sun_asia/sun_asia/templates/home.html')