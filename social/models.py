from django.db import models

class Social(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('pinterest', 'pinterest'),
        ('Youtube', 'Youtube'),
        # Add other platforms here
    ]

    name = models.CharField(max_length=100, choices=SOCIAL_CHOICES, default='facebook')
    url = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Social Icon'
        verbose_name_plural = "Social Icon's"

    def __str__(self):
        return self.name
