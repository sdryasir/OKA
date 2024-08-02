"""
URL configuration for oka_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('all-products/', views.fashion, name='products'),
    path('product-details/', views.productDetails, name='product-details'),
    path('search-results/', views.searchResult, name='search-results'),
    path('product-results/', views.productResult, name='product-results'),
    path('product-results/<category>', views.productResult, name='product-results'),
    path('register-user/', views.register_user, name='register-user'),
    path('login-user/', views.log_inUser, name='loginuser'),
    path('logout/', views.log_out_user, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Password_Reset_View.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)