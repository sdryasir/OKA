import nested_admin
from django.contrib import admin
from .models import Footer, FooterSection, FooterLink
from .models import Header
from .models import Footer


# class FooterAdmin(admin.ModelAdmin):
#     list_display = ['name' , 'url' , 'create']

# admin.site.register(Footer , FooterAdmin)


class HeaderAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "create"]


admin.site.register(Header, HeaderAdmin)

class FooterLinkInline(nested_admin.NestedTabularInline):
    model = FooterLink
    extra = 1

class FooterSectionInline(nested_admin.NestedStackedInline):
    model = FooterSection
    inlines = [FooterLinkInline]
    extra = 1

@admin.register(Footer)
class FooterAdmin(nested_admin.NestedModelAdmin):
    inlines = [FooterSectionInline]

