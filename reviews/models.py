from django.db import models
from django.contrib.auth.models import User
from orders.models import Orders
from Product.models import Products


# Create your models here.
class Reviews(models.Model):
    rating = models.IntegerField()
    opinion = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Item = models.ForeignKey("Product.Products", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Orders", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ("user", "Item", "order")

    def __str__(self):
        return f"Review by {self.user} for {self.Item} on {self.date_time}"
