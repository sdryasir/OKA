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
from django.urls import path, re_path, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    path('contact/', include('contact.urls'), name='contact'),
    path('faq', views.faq, name='faq'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('create_checkout_session', views.create_checkout_session, name='create_checkout_session'),
    path('all-products/', views.products, name='products'),
    path('resetfilter/', views.resetfilter, name='resetfilter'),
    path('product-details/<int:id>', views.product_details, name='product-details'),
    path('search-results/', views.searchResult, name='search-results'),
    path('product-results/', views.productResult, name='product-results'),
    path('submit_review/<int:id>/', views.submit_review, name='submit-review'),
    path('product-results/<int:category>', views.productResult, name='product-results'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('login-user/', views.log_inUser, name='loginuser'),
    path('logout/', views.log_out_user, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Password_Reset_View.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('order_status/', views.orderStatus, name='order_status'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    

]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)  