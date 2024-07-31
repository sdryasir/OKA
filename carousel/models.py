from django.db import models

class Carousel(models.Model):
    image = models.FileField(max_length=60 , upload_to= "products/")
