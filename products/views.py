from django.shortcuts import render
# from .models import Product
from django.shortcuts import get_object_or_404
from django.utils.timezone import now


# Create your views here.
def product_list(request):
    return render(request, 'product/product_list.html', {'timestamp': now().timestamp()})

def product_detail(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    return render(request, 'product/product_detail.html', {'timestamp': now().timestamp()})