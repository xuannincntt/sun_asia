from django.shortcuts import render
from accounts.models import User
from .models import Address, Order, OrderItem
from products.models import Product
from django.utils.timezone import now
from datetime import datetime
import json
from django.http import JsonResponse, HttpResponse
from .utils import generate_random_password, validate_order_form
import cloudinary.uploader
from sun_asia.utils import get_total_from_cart
from django.views.decorators.csrf import csrf_exempt
import uuid
from .utils import format_date_time

# Create your views here.
@csrf_exempt
def order(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    if request.method == "POST":
        address_mode = request.POST.get("addressMode")
        payment_mode  = request.POST.get("paymentMode")
        name = request.POST.get("name")
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        address = request.POST.get("address")
        city = request.POST.get("city")
        district = request.POST.get("district")
        notes = request.POST.get("notes")
        

        if request.POST.get("orderMode") == "buynow":
            order_items = request.session.get("buynow",[])
            # request.session["buynow"] = []
        else:
            order_items = request.session.get("cart",[])
            # request.session["cart"] = []
        # print("order_items", order_items)
        message = validate_order_form({
            'name': name,
            'email': email,
            'tel': tel,
            'address': address,
            'items': order_items
        })
        # print(message)
        if message:
            return JsonResponse({"message": message}, status=400)
        
        

        if not user: 
            user_from_email = User.objects.filter(email=email).first()

            if not user_from_email:
                user = User(
                    email=email,
                    tel=tel,
                    fixed_address=address
                )
                password = generate_random_password(8)
                user.set_password(password)
                user.save()
            else:
                user = user_from_email

        if address_mode == "DEFAULT":
            selected_address = Address.objects.filter(creator=user, is_default=True).first()
            if not selected_address:
                selected_address = Address(
                    creator=user,
                    name=name,
                    email=email,
                    tel=tel,
                    detailed_address=address,
                    city=city,
                    district=district,
                    is_default=True
                )
                selected_address.save()
            else:
                selected_address.name=name
                selected_address.email=email
                selected_address.tel=tel
                selected_address.detailed_address=address
                selected_address.city=city
                selected_address.district=district
                selected_address.updated_at=datetime.now()
                selected_address.save()
        else:
            selected_address = Address.objects.filter(
                creator=user,
                name=name,
                email=email,
                tel=tel,
                detailed_address=address,
                city=city,
                district=district
            )
            if not selected_address:
                selected_address = Address(
                    creator=user,
                    name=name,
                    email=email,
                    tel=tel,
                    detailed_address=address,
                    city=city,
                    district=district,
                    is_default=False
                )
                selected_address.save()

        image_url = None
        if request.FILES.get("bankProof"):
            bank_proof_image = request.FILES.get("bankProof")
            upload_result = cloudinary.uploader.upload(bank_proof_image)
            print(upload_result)
            image_url = upload_result.get('secure_url')

        # print(request.FILES.get("bankProof"))

        total_quantity, total_amount = get_total_from_cart(order_items)

        new_order = Order(
            order_address=selected_address,
            is_paid=True if image_url else False,
            payment=payment_mode,
            total_quantity=total_quantity,
            total_amount=total_amount,
            tax=0,
            discount=0,
            notes=notes,
            bank_proof=image_url if image_url else ""
        )
        new_order.save()

        for item in order_items:
            selected_product = Product.objects.filter(id=item["id"]).first()
            if not selected_product:
                return JsonResponse({"message":"Không tìm thấy sản phẩm này."}, status=404)

            new_item = OrderItem(
                order=new_order,
                product=selected_product,
                quantity=item["quantity"],
                price=item['price'],
                subtotal=item['subtotal']
            )
            new_item.save()

        request.session['new_order_uuid'] = str(new_order.uuid)

        # print("order_items", order_items)

        if request.POST.get("orderMode") == "buynow":
            request.session["buynow"] = []
        else:
            request.session["cart"] = []

        request.session['user_id'] = user.id

        return JsonResponse({
            "message":"Đặt hàng thành công",
            "order_uuid": new_order.uuid

            },status=201)
        
        
            


# def create_order(request):
#     user_id = request.session.get('user_id')
#     user = User.objects.get(id=user_id) if user_id else None
#     address = Address.objects.get(user=user_id) if user_id else {
#         'address': user.address if user else ''
#     }
#     if request.method == "POST":
#         return render(request, 'order/order_success.html')
#     return render(request, 'order/order.html', {'timestamp': now().timestamp(), 'user': user, 'address': address })

def order_success(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    new_order_uuid_str = request.session.get("new_order_uuid")

    if not new_order_uuid_str:
        return HttpResponse("Order not found", status=404)
    
    return render(request, 'order/order_success.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'order_uuid': new_order_uuid_str
        })


def order_history(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    lang_code = request.LANGUAGE_CODE

    selected_orders = Order.objects.filter(order_address__creator=user).order_by('-order_date','status')

    for selected_order in selected_orders:
        selected_items = OrderItem.objects.filter(order=selected_order)
        selected_order.order_items = selected_items
        selected_order.uuid_str = str(selected_order.uuid).replace("-","")
        selected_order.formatted_order_date = format_date_time(selected_order.order_date, lang_code)
        selected_order.total_amount_str = format(selected_order.total_amount,",")

        for item in selected_items:
            first_image = item.product.images.all().order_by('created_at').first()
            item.product.image_url = first_image.image_url if first_image else ""
    


    return render(request, 'order/order_history.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'orders': selected_orders
    })


def order_detail(request, order_uuid):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    formatted_order_uuid = uuid.UUID(order_uuid)

    selected_order = Order.objects.filter(uuid=formatted_order_uuid).first() if formatted_order_uuid else None
    
    if not selected_order:
        return HttpResponse("Order not found", status=400)
    print(selected_order.uuid)

    selected_order.uuid_str = str(selected_order.uuid).replace("-","")

    selected_order.total_amount_str = format(selected_order.total_amount,",")
    selected_order.tax_str = format(selected_order.tax,",")
    selected_order.discount_str = format(selected_order.discount, ",")
    selected_order.total_quantity_str = format(selected_order.total_quantity,",")
    selected_order.total_final_str = format(selected_order.total_amount + selected_order.tax - selected_order.discount, ",")
    
    selected_items = OrderItem.objects.filter(order=selected_order) if selected_order else None
    for item in selected_items:
        first_image = item.product.images.all().order_by('created_at').first()
        item.product.image_url = first_image.image_url if first_image else ""

    lang_code = request.LANGUAGE_CODE
    order_date = format_date_time(selected_order.order_date, lang_code)
    print(order_date)

    request.session["new_order_uuid"] = ""

    return render(request, 'order/order_detail.html', {
        'timestamp': now().timestamp(), 
        'user': user,
        'order_data': selected_order,
        'order_date': order_date,
        'order_items': selected_items
        })


