from django.db import models
class Category(models.Model):
    title = models.CharField(max_length=20)
    image = models.FileField(max_length=60 , upload_to= "products/")
    def __str__(self):
        return self.title
