from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    phone = models.IntegerField(blank=False, max_length=15)
    message = models.TextField(null=False, blank=False)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
