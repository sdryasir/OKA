from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_size(image):
    """Ensure the image size is 1920x800 pixels."""
    img = Image.open(image)
    if img.width != 1920 or img.height != 800:
        raise ValidationError("Image size must be 1920x800 pixels.")

class Offer(models.Model):
    title = models.CharField(max_length=30, null=True)
    image = models.FileField(
        max_length=60, 
        upload_to="products/", 
        help_text='Image size must be 1920x800 pixels',
        validators=[validate_image_size]
    )

    def __str__(self):
        return self.title
