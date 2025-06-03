from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new', views.create_order, name='create-order'),
    path('<int:order_id>', views.get_order_detail, name='order-detail')
]