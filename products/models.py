from django.db import models
from categories.models import Category


COLOR_CHOICES = (
    ('----','----'),
    ('In Stock', 'In Stock'),
    ('Out Of Stock','Out Of Stock'),
  
)

class Products(models.Model):
    title = models.CharField(max_length=50 , null=True)
    sub_title = models.TextField(max_length=250 , null=True)
    description = models.TextField(null=True)
    price_that_you_sell = models.IntegerField(help_text='the price that you sell' , null=True) 
    Orignal_price = models.IntegerField(help_text='this price is to attract the costumer and this is higher than price that you sell' , null=True)
    More_information = models.TextField(blank=True , null=True)
    availability = models.CharField(max_length=20, choices=COLOR_CHOICES, default='----' , null=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True)
    image = models.FileField(upload_to= "products/" , null=True , help_text='Image size must be 500 X 500 pixels')

 

    def __str__(self):
        return self.title

