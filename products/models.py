from django.db import models
from categories.models import Category

class Products(models.Model):
    title = models.CharField(max_length=50 , null=True)
    description = models.TextField(null=True)
    price_that_you_sell = models.IntegerField(help_text='the price that you sell' , null=True) 
    Orignal_price = models.IntegerField(help_text='this price is to attract the costumer and this is higher than price that you sell' , null=True)
    More_information = models.TextField(blank=True , null=True)
    In_Stock = models.IntegerField(null=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True)
    image = models.FileField(max_length=60 , upload_to= "products/" , null=True)

 

    def __str__(self):
        return self.title

