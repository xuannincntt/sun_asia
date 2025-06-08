from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('new', views.create_order, name='create-order'),
    path('<uuid:uuid>', views.get_order_detail, name='order-detail')
]