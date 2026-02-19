"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from django.shortcuts import render

def custom_404_view(request, exception):
    return render(request, 'shared/404.html', status=404)

handler404 = custom_404_view
urlpatterns = [
    path('', include('home_module.urls')),
    path('', include('acount_module.urls')),
    path('contact-us/',include('contact_us_module.urls')),
    path('products/', include('product_model.urls')),
    path('articles/',include('article_module.urls')),
    path('user/',include('user_module.urls')),
    path('order/',include('order_module.urls')),
    path('admin/', admin.site.urls)

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
