from django.db import models

class Carousel(models.Model):
    title = models.CharField(max_length=30 , null=True)
    image = models.FileField(max_length=60 , upload_to= "products/")

