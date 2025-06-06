"""
URL configuration for sun_asia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.i18n import set_language
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('news/', include('news.urls')),
    path('projects/', include('projects.urls')),
    path('contact/', include('contact.urls')),
    path('cart/', views.cart, name='cart'),
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('set_language/', set_language, name='set_language'),
    path('tinymce/', include('tinymce.urls')),
]
