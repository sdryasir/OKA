from django.db import models

class Carousel(models.Model):
    title = models.CharField(max_length=30 , null=True)
    image = models.FileField(max_length=60 , upload_to= "products/" , help_text='Image size must be 1920 X 1080 pixels')

