from django.shortcuts import render
from accounts.models import User
from .models import Address, Order, OrderItem
from django.utils.timezone import now
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
def order(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    if request.method == "POST":
        address_mode = request.POST.get("addressMode")
        name = request.POST.get("name")
        email = request.POST.get("email")
        tel = request.POST.get("tel")
        address = request.POST.get("address")
        city = request.POST.get("city")
        district = request.POST.get('district')

        order = request.session.get("buynow",[])
        if len(order) == 0:
            return HttpResponse({"message": "Bạn chưa đặt mặt hàng nào."})

        if not user: 
            user = User(
                email=email,
                tel=tel,
                fixed_address=address
            )
            user.save()

        if address_mode == "DEFAULT":
            selected_address = Address.objects.filter(creator=user, is_default=True).first()
            if not selected_address:
                selected_address = Address(
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
        else:
            selected_address = Address.objects.filter(
                name=name,
                email=email,
                tel=tel,
                detailed_address=address,
                city=city,
                district=district
            )
            if not selected_address:
                selected_address = Address(
                    name=name,
                    email=email,
                    tel=tel,
                    detailed_address=address,
                    city=city,
                    district=district,
                    is_default=False
                )
                selected_address.save()
        
        
            


# def create_order(request):
#     user_id = request.session.get('user_id')
#     user = User.objects.get(id=user_id) if user_id else None
#     address = Address.objects.get(user=user_id) if user_id else {
#         'address': user.address if user else ''
#     }
#     if request.method == "POST":
#         return render(request, 'order/order_success.html')
#     return render(request, 'order/order.html', {'timestamp': now().timestamp(), 'user': user, 'address': address })

def get_order_detail(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    return render(request, 'order/order_detail.html', {'timestamp': now().timestamp(), 'user': user})
