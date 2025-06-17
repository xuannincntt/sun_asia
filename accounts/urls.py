from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('update-avatar/', views.update_avatar, name='update-avatar'),
    path('update-name/', views.update_name, name='update-name'),
    path('update-email/', views.update_email, name='update-email'),
    path('check-password/', views.check_password, name='check-password'),
    path('update-password/', views.update_password, name='update-password'),
    path('update-phone/', views.update_phone, name='update-phone'),
    path('create-address/', views.create_address, name='create-address'),
    path('update-address/', views.update_address, name='update-address'),
    path('delete-address/', views.delete_address, name='delete-address'),
    path('set-default-address/', views.set_default_address, name='set_default_address'),
    path('<slug:slug>/', views.user_profile_view, name='user-profile'),
]