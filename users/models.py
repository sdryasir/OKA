from django.db import models
from django.contrib.auth.models import User
class Userdata(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    country = models.CharField(max_length=50 , null=True)
    address = models.CharField(max_length=100 , null=True)
    city = models.CharField(max_length=50 , null=True)
    state = models.CharField(max_length=50 , null=True)
    zip_code = models.CharField(max_length=50 , null=True)
    phone_no = models.CharField(max_length=18 , null=True)
    profile_picture = models.ImageField(upload_to='products/', null=True, blank=True)

