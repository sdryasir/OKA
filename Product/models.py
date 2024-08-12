from django.db import models
from categories.models import Category


COLOR_CHOICES = (
    ('----','----'),
    ('In Stock', 'In Stock'),
    ('Out Of Stock','Out Of Stock'),
  
)

class Products(models.Model):
    name = models.CharField(max_length=50 , null=True)
    sub_title = models.TextField(max_length=250 , null=True)
    description = models.TextField(null=True)
    price_that_you_sell = models.IntegerField(help_text='the price that you sell' , null=True) 
    Orignal_price = models.IntegerField(help_text='this price is to attract the costumer and this is higher than price that you sell' , null=True)
    More_information = models.TextField(blank=True , null=True)
    availability = models.CharField(max_length=20, choices=COLOR_CHOICES, default='----' , null=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True)
    image = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')
    image2 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')
    image3 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')
    image4 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')
    image5 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')
    image6 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times')

 

    def __str__(self):
        return self.title

