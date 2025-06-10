from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('success', views.order_success, name='order-success'),
    path('history', views.order_history, name='order-history'),
    path('detail', views.order_detail, name='order-detail')
]