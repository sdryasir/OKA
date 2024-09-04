from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image
from categories.models import Category


COLOR_CHOICES = (
    ('----','----'),
    ('In Stock', 'In Stock'),
    ('Out Of Stock','Out Of Stock'),
  
)

def validate_image_size(image):
    """Ensure the image size is 500x500 pixels."""
    img = Image.open(image)
    if img.width != 500 or img.height != 500:
        raise ValidationError("Image size must be 500x500 pixels.")
        

class Products(models.Model):
    name = models.CharField(max_length=50 , null=True)
    sub_title = models.TextField(max_length=250 , null=True)
    description = models.TextField(null=True)
    price = models.IntegerField(help_text='the price that you sell' , null=True) 
    discount_price = models.IntegerField(blank = True , help_text='this price is to attract the costumer and this is higher than price that you sell' , null=True)
    More_information = models.TextField(blank=True , null=True)
    availability = models.CharField(max_length=20, choices=COLOR_CHOICES, default='----' , null=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True)
    image = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' , validators=[validate_image_size]) 
    image2 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' ,  validators=[validate_image_size])
    image3 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' ,  validators=[validate_image_size])
    image4 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' ,  validators=[validate_image_size])
    image5 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' ,  validators=[validate_image_size])
    image6 = models.FileField(upload_to= "products/" , max_length=200 , null=True , help_text='Image size must be 500 X 500 pixels and add all images. If you dont have enough images then you can add 1 image 6 times' ,  validators=[validate_image_size])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
