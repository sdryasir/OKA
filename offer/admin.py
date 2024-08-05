from django.contrib import admin
from .models import Offer

class offerAdmin(admin.ModelAdmin):
    
    list_display = ['title' , 'image' ,]

admin.site.register(Offer , offerAdmin)
