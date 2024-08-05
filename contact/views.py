from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    return render(request, 'contact.html')

def savecontact(request):
    # Check honeypot fields
    if request.POST.get('honeypot_name') or request.POST.get('honeypot_email'):
        return render(request, 'contact.html', {'error': 'Bot detected'})

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message = request.POST.get('message')
    
    # Check if required fields are filled
    if not name or not email or not phone or not message:
        messages.error(request, 'Please Fill All The Fields!')
        return render(request, 'contact.html')
    else:
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, 'Sent Successfully!')
        return redirect('contact')  # Redirect to the contact page or another page of your choice
