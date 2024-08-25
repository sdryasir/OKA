from .models import Social

def socials(request):
    socials = Social.objects.all()
    return {'social': socials}