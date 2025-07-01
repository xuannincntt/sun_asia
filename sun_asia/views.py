from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from accounts.models import User
from order.models import Address, Order, OrderItem
from products.models import Product, Category, ProductImage
from projects.models import Project
from django.utils.timezone import now
from django.views.decorators.cache import never_cache
from django.db.models import Prefetch
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import get_total_from_cart

image_prefetch = Prefetch(
    'images',
    queryset=ProductImage.objects.order_by('created_at'),
    to_attr='prefetched_images'
)

def home(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    top_projects = Project.objects.order_by('-area')[:4]
    sort = request.GET.get('sort', 'newest')
    if sort == 'bestseller':
        products = Product.objects.all().order_by('-sold')[:8]
    else:
        products = Product.objects.all().order_by('-created_at')[:8]
    for product in products:
        first_image = product.images.all().order_by('created_at').first()
        product.image_url = first_image.image_url if first_image else ""
        product.org_price = format(product.org_price if product.org_price > 0 else 0, ",")
        product.sale_price = format(product.sale_price if product.sale_price >= 0 else -1, ",")
    for project in top_projects:
        project.area = format(project.area if project.area > 0 else 0, ",")
    return render(request, 'home.html', {
        'sort': sort,
        'products': products,
        'top_projects': top_projects,
        'timestamp': now().timestamp(),
        'user': user})

@never_cache
def product_by_category(request, cat_slug):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    category = Category.objects.filter(slug=cat_slug).first() if cat_slug else None
    
    categories = Category.objects.all()

    if category:
        products = Product.objects.filter(category=category).prefetch_related(image_prefetch)

        for product in products:
            first_image = product.images.all().order_by('created_at').first()
            product.image_url = first_image.image_url if first_image else ""
            product.org_price = format(product.org_price if product.org_price > 0 else 0, ",")
            product.sale_price = format(product.sale_price if product.sale_price >= 0 else -1, ",")
    else:
        products = None

    
    # print(list(products))

    return render(request, 'product/product_list.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'products': products,
        'selected_category': category if category else {
            'slug': "tat-ca-san-pham"
        },
        'categories': categories})

def logout_view(request):
    del request.session['user_id']
    return redirect('/')

@never_cache
@csrf_exempt
def cart(request):
    cart = request.session.get('cart',[])
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_slug = data.get('productSlug')
            product_id = data.get('productId')

            # Lấy sản phẩm trong bảng
            selected_product = Product.objects.filter(slug=product_slug).first() if product_slug else None
            if not selected_product:
                selected_product = Product.objects.filter(id=product_id).first()

            if not selected_product:
                return JsonResponse({'message': 'Không tìm thấy sản phẩm này.'}, status=404)
            
            # Kiểm tra sản phẩm có trong cart chưa
            cart_len = len(cart)
            product_index_in_cart = cart_len
            for index in range(0,cart_len):
                if cart[index]['id'] == selected_product.id or cart[index]['slug'] == selected_product.slug:
                    product_index_in_cart = index
                    break

            print(product_index_in_cart)

            if product_index_in_cart == cart_len:
                first_image = selected_product.images.all().order_by('created_at').first()
                sale_price = selected_product.sale_price
                org_price = selected_product.org_price
                selected_price = sale_price if sale_price >= 0 and sale_price != org_price else org_price
                new_item = {
                    "id": selected_product.id,
                    "name": selected_product.name,
                    "slug": selected_product.slug,
                    "price": selected_price,
                    "image_url": first_image.image_url if first_image else "",
                    "quantity": 1,
                    "subtotal": selected_price,
                    "quantity_text": format(1,","),
                    "price_text": format(selected_price,","),
                    "subtotal_text": format(selected_price,",")
                }
                cart.append(new_item)        

            else:
                current_quantity = cart[product_index_in_cart]['quantity']
                cart[product_index_in_cart]['quantity'] = current_quantity + 1
                cart[product_index_in_cart]['quantity_text'] = format(current_quantity + 1,",")
                price = cart[product_index_in_cart]['price']
                cart[product_index_in_cart]['subtotal'] = (current_quantity + 1)*price
                

            request.session['cart'] = cart
            return JsonResponse({'message': 'Thêm vào giỏ hàng thành công!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Có lỗi xảy ra. Hãy thử lại sau.'}, status=400)
    
    total_quantity, total_temp = get_total_from_cart(cart)
    total_vat = 0
    total_discount = 0

    return render(request, 'cart.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'cart': {
            'cart_items': cart,
            'total_quantity': format(total_quantity,","),
            'total_temp': format(total_temp,","),
            'total_vat': format(total_vat,","),
            'total_discount': format(total_discount,","),
            'total_final': format(total_temp + total_vat - total_discount,",")
        }})

@never_cache
@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            updated_cart_data = data.get('cart')
            updated_cart = []
            for item in updated_cart_data:
                product_id = item['productId']
                # Lấy sản phẩm trong bảng
                selected_product = Product.objects.filter(id=product_id).first()

                if not selected_product:
                    return JsonResponse({'message': 'Không tìm thấy sản phẩm này.'}, status=404)
                
                first_image = selected_product.images.all().order_by('created_at').first()
                sale_price = selected_product.sale_price
                org_price = selected_product.org_price
                selected_price = sale_price if sale_price >= 0 and sale_price != org_price else org_price

                product_quantity = item['productQuantity']
                new_item = {
                    "id": selected_product.id,
                    "name": selected_product.name,
                    "slug": selected_product.slug,
                    "price": selected_price,
                    "image_url": first_image.image_url if first_image else "",
                    "quantity": product_quantity if product_quantity else 1,
                    "subtotal": selected_price,
                    "quantity_text": format(product_quantity if product_quantity else 1,","),
                    "price_text": format(selected_price,","),
                    "subtotal_text": format(selected_price,",")
                }
                updated_cart.append(new_item)

            request.session['cart'] = updated_cart
            return JsonResponse({
                'message': 'Cập nhật giỏ hàng thành công!',
                }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Có lỗi xảy ra: Không lấy được dữ liệu JSON'}, status=400)

@never_cache
@csrf_exempt
def checkout(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    cart = request.session.get('cart',[])
    try:
        default_address = Address.objects.filter(creator=user, is_default=True).first() if user else None
    except:
        default_address = None
    if request.method == "POST":
        product_id = request.POST.get('productId')
        product_quantity = int(request.POST.get('productQuantity'))

        selected_product = Product.objects.filter(id=product_id).first() if product_id else None
        if not selected_product:
            return HttpResponse({'message': 'Không tìm thấy sản phẩm này.'}, status=404)
        
        first_image = selected_product.images.all().order_by('created_at').first()
        sale_price = selected_product.sale_price
        org_price = selected_product.org_price
        selected_price = sale_price if sale_price >= 0 and sale_price != org_price else org_price
        order_items = [
            
            {
                "id": selected_product.id,
                "name": selected_product.name,
                "slug": selected_product.slug,
                "price": selected_price,
                "image_url": first_image.image_url if first_image else "",
                "quantity": product_quantity,
                "subtotal": product_quantity*selected_price,
                "quantity_text": format(product_quantity,","),
                "price_text": format(selected_price,","),
                "subtotal_text": format(selected_price,",")
            }
        ]
        total_quantity, total_temp = get_total_from_cart(order_items)
        total_vat = 0
        total_discount = 0

        request.session['buynow'] = order_items

        return render(request, 'checkout.html',
            {
            'timestamp': now().timestamp(), 
            'user': user, 
            'default_address': default_address,
            'order_mode': 'buynow',
            'order': {
                'order_items': order_items,
                'total_quantity': format(total_quantity,","),
                'total_temp': format(total_temp,","),
                'total_vat': format(total_vat,","),
                'total_discount': format(total_discount,","),
                'total_final': format(total_temp + total_vat - total_discount,",")
            }})
    
    total_quantity, total_temp = get_total_from_cart(cart)
    total_vat = 0
    total_discount = 0
    # print(default_address.email)
    

    return render(request, 'checkout.html', {
        'timestamp': now().timestamp(), 
        'user': user, 
        'default_address': default_address,
        'order_mode': 'cart',
        'order': {
            'order_items': cart,
            'total_quantity': format(total_quantity,","),
            'total_temp': format(total_temp,","),
            'total_vat': format(total_vat,","),
            'total_discount': format(total_discount,","),
            'total_final': format(total_temp + total_vat - total_discount,",")
        }})

@never_cache
def favorite(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'favorite.html', {'user': user})