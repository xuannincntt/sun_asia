from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from accounts.models import User
from .models import News, NewsCategory
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache

@never_cache
def news(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None

    all_news = News.objects.order_by('-published_at')
    most_viewed_news = News.objects.order_by('-views')[:4]
    latest_news = all_news[:3]

    categories = NewsCategory.objects.all()
    selected_categories = request.GET.getlist('category')

    if selected_categories:
        filtered_news = all_news.filter(category_id__in=selected_categories)
        other_news = filtered_news.exclude(id__in=latest_news.values_list('id', flat=True))
    else:
        other_news = all_news.exclude(id__in=latest_news.values_list('id', flat=True))

    # Phân trang: 4 bài viết mỗi trang
    paginator = Paginator(other_news, 4)  # 4 bài mỗi trang
    page_number = request.GET.get('page')
    other_news = paginator.get_page(page_number)  # projects chính là page object bạn đã dùng trong template

    return render(request, 'news/news.html', {
        'timestamp': now().timestamp(),
        'user': user,
        'latest_news': latest_news,
        'most_viewed_news': most_viewed_news,
        'categories': categories,
        'selected_categories': [str(cat_id) for cat_id in selected_categories],
        'other_news': other_news,
    })

@never_cache
def news_detail(request, slug):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id) if user_id else None
    most_viewed_news = News.objects.order_by('-views')[:4]
    try:
        news_item = News.objects.get(slug=slug)
        news_item.views += 1
        news_item.save()
    except News.DoesNotExist:
        return redirect('news:news')
    return render(request, 'news/news_detail.html', {
        'timestamp': now().timestamp(),
        'most_viewed_news': most_viewed_news,
        'user': user,
        'news_item': news_item,
    })