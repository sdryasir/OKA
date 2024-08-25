from django.db import models


# class Footer(models.Model):
#         name = models.CharField(blank=False, max_length=100,null=True)
#         url = models.URLField(blank=False, null=True)
#         create = models.DateField(auto_now_add=True, null=True)
    
#         def __str__(self):
#             return self.name

class Header(models.Model):
    name = models.CharField(blank=False, max_length=100,null=True)
    url = models.URLField(blank=False)
    create = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Footer(models.Model):
    title = models.CharField(max_length=100,  unique=True, default="Default Footer Title")

    def __str__(self):
        return self.title

class FooterSection(models.Model):
    footer = models.ForeignKey(Footer, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.footer.title} - {self.title}"

class FooterLink(models.Model):
    section = models.ForeignKey(FooterSection, related_name='links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Name Here')
    url = models.URLField(help_text='URL Here')

    def __str__(self):
        return f"{self.name} ({self.section.title})"


