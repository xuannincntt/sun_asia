from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('<slug:slug>/', views.user_profile_view, name='user-profile'),
]