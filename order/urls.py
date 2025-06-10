from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('success', views.order_success, name='order-success'),
    path('<uuid:uuid>', views.order_detail, name='order-detail')
]