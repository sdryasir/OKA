from . import views
from django.urls import path, re_path
from django.conf import settings

urlpatterns = [
    path('', views.faq, name=''),
]