from django.shortcuts import render, redirect
from .models import User
from order.models import Address
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.hashers import make_password
import uuid
from django.utils.timezone import now
from django.http import JsonResponse
import cloudinary.uploader
import json
from django.db.models import Q

@never_cache
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
    return render(request, 'accounts/accounts.html', {
        'timestamp': now().timestamp(),
        'user': user})

@never_cache
def user_profile_view(request, slug):
    # Lấy thông tin user đang đăng nhập từ session
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    if not user or user.slug != slug:
        return render(request, '404.html', {'user': user})
    return render(request, 'accounts/information.html', {
        'timestamp': now().timestamp(),
        'user': user})

@never_cache
def update_avatar(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User ID not in session'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    if 'avatar' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No avatar file provided'})
    avatar = request.FILES['avatar']
    try:
        result = cloudinary.uploader.upload(avatar, folder='avatars')
        user.avatar_url = result['secure_url']
        user.save()
        return JsonResponse({'success': True, 'avatar_url': result['secure_url']})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@never_cache
def update_name(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User ID not in session'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    try:
        data = json.loads(request.body)
        new_username = data.get('newname', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    if not new_username:
        return JsonResponse({'success': False, 'error': 'Username cannot be empty'})
    user.username = new_username
    user.save()
    return JsonResponse({'success': True, 'username': new_username})

@never_cache
def update_email(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User ID not in session'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    try:
        data = json.loads(request.body)
        new_email = data.get('newemail', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    if not new_email:
        return JsonResponse({'success': False, 'error': 'Email cannot be empty'})
    # Kiểm tra email đã tồn tại và không phải của chính user hiện tại
    if User.objects.filter(Q(email=new_email) & ~Q(id=user_id)).exists():
        return JsonResponse({'success': False, 'error': 'Email already exists'})
    user.email = new_email
    user.save()
    return JsonResponse({'success': True, 'email': new_email})

@never_cache
def check_password(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User not logged in'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    try:
        data = json.loads(request.body)
        password = data.get('password', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    if not django_check_password(password, user.password):
        return JsonResponse({'success': False, 'error': 'Mật khẩu không đúng!'})
    return JsonResponse({'success': True})

@never_cache
def update_password(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User not logged in'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    try:
        data = json.loads(request.body)
        new_password = data.get('newpassword', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    if len(new_password) < 6:
        return JsonResponse({'success': False, 'error': 'Mật khẩu mới phải có ít nhất 6 ký tự'})
    user.password = make_password(new_password)
    user.save()
    return JsonResponse({'success': True, 'pass': new_password})

@never_cache
def update_phone(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User ID not in session'})
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    try:
        data = json.loads(request.body)
        new_phone = data.get('newphone', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    if not new_phone:
        return JsonResponse({'success': False, 'error': 'Username cannot be empty'})
    user.tel = new_phone
    user.save()
    return JsonResponse({'success': True, 'phone': new_phone})


@never_cache
def update_address(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ!'})
    try:
        # Lấy user từ session
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'error': 'Người dùng chưa đăng nhập!'})
        user = User.objects.get(id=user_id)
        # Đọc dữ liệu JSON gửi lên
        body = json.loads(request.body)
        province = body.get('province')
        district = body.get('district')
        ward = body.get('ward')
        detail = body.get('detail')
        # Validate đơn giản
        if not all([province, district, ward, detail]):
            return JsonResponse({'success': False, 'error': 'Vui lòng điền đầy đủ thông tin!'})
        Address.objects.create(
            creator=user,
            name=user.username,
            detailed_address=detail,
            city=province,
            district=district,
            ward=ward,
            tel=user.tel, 
            email=user.email, 
            is_default=True 
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})