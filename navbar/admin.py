from django.contrib import admin
from .models import Navbar

class NavBarAdmin(admin.ModelAdmin):
    list_display = ['name' , 'url' , 'create']

admin.site.register(Navbar , NavBarAdmin)
