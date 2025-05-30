from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

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
                    request.session['user_id'] = user.id  # Lưu vào session
                    messages.success(request, f"Chào mừng {user.username or user.email}!")
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
                new_user = User(
                    username=username,
                    email=email,
                )
                new_user.set_password(password)
                new_user.save()
                messages.success(request, "Đăng ký thành công! Mời đăng nhập.")
                return redirect('/')
    return render(request, 'accounts/accounts.html', {'user': user})