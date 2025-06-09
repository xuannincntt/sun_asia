from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from accounts.models import User
from .models import Project
from django.utils.timezone import now
from django.db.models import Q
from django.core.paginator import Paginator

def projects(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    all_projects = Project.objects.all()

    # --- Tách tỉnh thành ---
    raw_cities = all_projects.values_list('city', flat=True)
    provinces = set()
    for city in raw_cities:
        if city:
            parts = city.split('-')
            province = parts[-1].strip()
            provinces.add(province)

    # --- Các lựa chọn lọc ---
    selected_tinh_thanh = request.GET.get('tinh_thanh')
    selected_products = request.GET.getlist('product')
    selected_area_ranges = request.GET.getlist('project_type')

    # --- Lọc theo tỉnh thành ---
    projects = all_projects
    if selected_tinh_thanh:
        projects = projects.filter(city__icontains=selected_tinh_thanh)

    # --- Lọc theo sản phẩm ---
    if selected_products:
        for sp in selected_products:
            projects = projects.filter(product__icontains=sp)

    # --- Lọc theo diện tích ---
    if selected_area_ranges:
        area_filters = Q()
        for r in selected_area_ranges:
            if r.endswith('-'):
                max_val = int(r[:-1])
                area_filters |= Q(area__lt=max_val)
            elif r.endswith('+'):
                min_val = int(r[:-1])
                area_filters |= Q(area__gte=min_val)
            elif '-' in r:
                parts = r.split('-')
                if len(parts) == 2:
                    min_val = int(parts[0])
                    max_val = int(parts[1])
                    area_filters |= Q(area__gte=min_val, area__lt=max_val)
        projects = projects.filter(area_filters)

    # --- Trích danh sách sản phẩm ---
    raw_products = all_projects.values_list('product', flat=True)
    product_set = set()
    for p in raw_products:
        if p:
            items = [i.strip() for i in p.split(',')]
            product_set.update(items)
    projects = list(projects)  # đảm bảo là list, không phải QuerySet

    paginator = Paginator(projects, 4)  # 4 project mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'projects': page_obj,
        'provinces': sorted(provinces),
        'selected_tinh_thanh': selected_tinh_thanh,
        'product_list': sorted(product_set),
        'selected_products': selected_products,
        'selected_area_ranges': selected_area_ranges,
    }
    return render(request, 'projects/projects.html', context)