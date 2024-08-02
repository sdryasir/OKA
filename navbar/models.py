from django.db import models

class Navbar(models.Model):
    name = models.CharField(blank=False, max_length=10)
    url = models.URLField(blank=False)
    create = models.DateField(auto_now_add=True)