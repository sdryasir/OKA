from django.db import models
from django.contrib.auth.models import User
from orders.models import Orders
from Product.models import Products


class Reviews(models.Model):
    rating = models.IntegerField()
    opinion = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Item = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ("user", "Item", "order")

    def __str__(self):
        return f"Review by {self.user} for {self.Item} on {self.date_time}"
