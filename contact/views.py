from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Contact

def contact(request):
    return render(request, 'contact.html')

def savecontact(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    if not name or not email or not phone or not message:
        messages.error(request,'Please Fill All The FIelds!')
        return render(request, 'contact.html') 
    else:
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request,'Send Successfully!')
        return render(request, 'contact.html') 