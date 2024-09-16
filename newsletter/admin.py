from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionModelAdmin
from .models import Newsletter

class NewsletterResource(resources.ModelResource):
    class Meta:
        model = Newsletter

class NewsletterAdmin(ExportActionModelAdmin):
    resource_class = NewsletterResource
    list_display = ['email']
    # Optional: Add filtering options here

admin.site.register(Newsletter, NewsletterAdmin)
