from django.contrib import admin
from .models import Contact,Usrinfo

class ContactAdmin(admin.ModelAdmin):
    
    list_display = ['name' , 'email']
    
class UsrinfoAdmin(admin.ModelAdmin):
    
    list_display = ['email' , 'phone']

admin.site.register(Contact , ContactAdmin)
admin.site.register(Usrinfo, UsrinfoAdmin)
