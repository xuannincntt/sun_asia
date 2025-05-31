from django.shortcuts import render
# from .models import Product
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now


# Create your views here.
def product_list(request):
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'product/product_list.html', {'timestamp': now().timestamp(), 'user': user})

def product_detail(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'product/product_detail.html', {'timestamp': now().timestamp(), 'user': user})