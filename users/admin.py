from django.contrib import admin
from .models import Userdata
class offerAdmin(admin.ModelAdmin):
    
    list_display = ['user' , 'country' , 'address' , 'city' , 'state' , 'zip_code' , 'phone_no']

admin.site.register(Userdata , offerAdmin)
