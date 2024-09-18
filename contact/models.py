from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    phone = models.CharField(blank=False, max_length=15)
    message = models.TextField(null=False, blank=False)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
class Usrinfo(models.Model):
    phone = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    email2 = models.EmailField(max_length=100, blank=True,null=True)
    address = models.TextField(null=False, blank=False)
    working_hours = models.CharField(null=True, blank=False, max_length=50)
    info = models.TextField(null=True, blank=False)
    map_link = models.TextField(null=False, blank=False)  

    class Meta:
        verbose_name_plural = "Admin info's"
        verbose_name = "Admin info"

    def __str__(self):
        return self.email
