from django.db import models
from django.contrib.auth.models import User

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20 , default="Pending")
    payment_status = models.CharField(max_length=20 , default="unpaid" , null=True)
    payment_id = models.CharField(max_length=100,null=True)
    total_price = models.DecimalField(max_digits=10 , decimal_places=2 , default=0.00)
    class Meta:
        verbose_name_plural = "Order"
    def __str__(self):
        return f"Order {self.id} by {self.user}"
class OrderItem(models.Model):
    order = models.ForeignKey(Orders , on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10 , decimal_places=2 , default=0.00)
    def __str__(self):
        return f"{self.quantity} x {self.product_name} (order {self.order.id})"