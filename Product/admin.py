from django.contrib import admin
from .models import Products
class productAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price' , 'availability' , 'category']

admin.site.register(Products , productAdmin)
