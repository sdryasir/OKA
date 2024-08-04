from django.contrib import admin
from .models import Faq

class FaqAdmin(admin.ModelAdmin):
    list_display = ['Question', 'Answer', 'created']

admin.site.register(Faq , FaqAdmin)
