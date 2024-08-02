# from django.db import models
# from categories.models import Category

# class Products(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     price = models.IntegerField() 
#     compare_price = models.IntegerField()
#     More_information = models.TextField(blank=True)
#     In_Stock = models.IntegerField(null=True)
#     category = models.ForeignKey(Category , on_delete=models.CASCADE)
#     image = models.FileField(max_length=60 , upload_to= "products/")

#     def __str__(self):
#         return self.title

