from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from order.models import Address
from django.contrib import messages
from django.utils.text import slugify
import uuid

def accounts(request):
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    if request.method == 'POST':
        # === XỬ LÝ ĐĂNG NHẬP ===
        if 'login' in request.POST:
            email = request.POST.get('login_email')
            password = request.POST.get('login_password')
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    return redirect('/')
                else:
                    messages.error(request, "Mật khẩu không đúng.")
            except User.DoesNotExist:
                messages.error(request, "Tài khoản không tồn tại.")
        # === XỬ LÝ ĐĂNG KÝ ===
        elif 'register' in request.POST:
            username = request.POST.get('reg_username')
            email = request.POST.get('reg_email')
            password = request.POST.get('reg_password')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email đã được sử dụng.")
            else:
                # Tạo slug từ username
                base_slug = slugify(username)
                slug = base_slug
                while User.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                # Tạo và lưu user mới
                new_user = User(
                    username=username,
                    email=email,
                    slug=slug
                )
                new_user.set_password(password)
                new_user.save()
                # Lưu ID vào session
                request.session['user_id'] = new_user.id

                # Tạo địa chỉ nhận hàng đầu tiên ngay khi đăng kí
                default_address = Address.objects.filter(creator=new_user, is_default=True).first() if new_user else None
                if not default_address:
                    new_address = Address(
                        creator=new_user,
                        email=email,
                        is_default=True
                    )
                    new_address.save()
                
                return redirect('/')
    return render(request, 'accounts/accounts.html', {'user': user})

def user_profile_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, 'accounts/information.html', {'user': user})