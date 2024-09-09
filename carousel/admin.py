from django.contrib import admin
from .models import Carousel
class carouselAdmin(admin.ModelAdmin):
    list_display = ['title' ,'image']
admin.site.register(Carousel , carouselAdmin)