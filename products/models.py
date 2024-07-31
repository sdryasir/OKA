from django.db import models
from categories.models import Category

class Products(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField() 
    compare_price = models.IntegerField(blank=True)
    More_information = models.TextField(blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    image = models.FileField(max_length=60 , upload_to= "products/")

