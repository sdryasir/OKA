from django.shortcuts import render
from faq.models import Faq
# Create your views here.

def faq(request):
    faq = Faq.objects.all()
    data = {
        "faq" : faq
    }
    return render(request, "faq.html", data)
