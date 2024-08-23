from django.contrib import admin
from .models import Header
from .models import Footer


class FooterAdmin(admin.ModelAdmin):
    list_display = ['name' , 'url' , 'create']

admin.site.register(Footer , FooterAdmin)


class HeaderAdmin(admin.ModelAdmin):
    list_display = ['name' , 'url' , 'create']

admin.site.register(Header , HeaderAdmin)


