from django.db import models
class Category(models.Model):
    title = models.CharField(max_length=20)
    image = models.FileField(max_length=60 , upload_to= "products/" , help_text='Image size must be 500 X 500 pixels')
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.title
