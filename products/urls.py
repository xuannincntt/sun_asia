from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # path('',views.product_by_category, name='product-by-category'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]