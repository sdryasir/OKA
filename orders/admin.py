from django.contrib import admin
from .models import Orders , OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , 'created_at' , 'updated_at' , 'status' , 'total_price' , 'payment_status' , 'payment_id']

admin.site.register(Orders , OrderAdmin)


# Register your models here.
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order' , 'product_name' , 'quantity' , 'price']

admin.site.register(OrderItem , OrderItemAdmin)
