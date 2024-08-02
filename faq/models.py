from django.db import models

class Faq(models.Model):
    Question = models.TextField(blank=False)
    Answer = models.TextField(blank=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Question

