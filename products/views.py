from django.shortcuts import render
# from .models import Product
from .models import Product, ProductImage
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Prefetch


image_prefetch = Prefetch(
    'images',
    queryset=ProductImage.objects.order_by('created_at'),
    to_attr='prefetched_images'
)


# Create your views here.
def product_list(request):
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    products = Product.objects.all().prefetch_related(image_prefetch)

    for product in products:
        first_image = product.images.all().order_by('id').first()
        product.image_url = first_image.image_url if first_image else ""
    
    print(list(products))

    return render(request, 'product/product_list.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'products': products})

def product_detail(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    
    return render(request, 'product/product_detail.html', {
        'timestamp': now().timestamp(), 
        'user': user})
