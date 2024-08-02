from django.contrib import admin
from .models import Products
class productAdmin(admin.ModelAdmin):
    list_display = ['title' , 'price' , 'category']

admin.site.register(Products , productAdmin)
