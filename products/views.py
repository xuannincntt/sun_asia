from django.shortcuts import render
# from .models import Product
from .models import Product, ProductImage, Category
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator



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
    category_slug = request.GET.get('category', 'all')
    print(category_slug)
    categories = Category.objects.all()
    selected_category = {
        'name': "Tất cả sản phẩm",
        'slug': "tat-ca-san-pham"
    }
    if category_slug == 'all':
        products = Product.objects.all().prefetch_related(image_prefetch)
        for product in products:
            first_image = product.images.all().order_by('created_at').first()
            product.image_url = first_image.image_url if first_image else ""
            product.org_price = format(product.org_price if product.org_price > 0 else 0, ",")
            product.sale_price = format(product.sale_price if product.sale_price >= 0 else -1, ",")
    else:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if not selected_category:
            return HttpResponse({"message: Category not found"}, status=404)
        products = Product.objects.filter(category=selected_category).prefetch_related(image_prefetch)
        for product in products:
            first_image = product.images.all().order_by('created_at').first()
            product.image_url = first_image.image_url if first_image else ""
            product.org_price = format(product.org_price if product.org_price > 0 else 0, ",")
            product.sale_price = format(product.sale_price if product.sale_price >= 0 else -1, ",")
    # print(list(products))
    # phân trang
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'product/product_list.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'selected_category': selected_category,
        'products': products,
        'categories': categories})

def product_detail(request, slug):
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    product = Product.objects.filter(slug=slug).first() if slug else None
    product.org_price = format(product.org_price if product.org_price > 0 else 0, ",")
    print(product.org_price)
    product.sale_price = format(product.sale_price if product.sale_price >= 0 else -1, ",")
    print(product.sale_price)

    product_images = ProductImage.objects.filter(product=product) if product else None

    # print(dict(product))
    # print(list(product_images))
    
    return render(request, 'product/product_detail.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'product': product,
        'product_images': product_images})
