from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError
import requests
import json
from .models import Contact, Usrinfo

def contact(request):
    info = Usrinfo.objects.all()
    data = {
        "info": info,
    }
    return render(request, 'contact.html', data)

def savecontact(request):
    d = Usrinfo.objects.all()

    # Honeypot fields to detect bots
    if request.POST.get('honeypot_name') or request.POST.get('honeypot_email'):
        return render(request, 'contact.html', {'error': 'Bot detected'})

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message = request.POST.get('message')

    # Check if required fields are filled
    if not name or not email or not phone or not message:
        messages.error(request, 'Please Fill All The Fields!')
        return render(request, 'contact.html', {'info': d})

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address!')
        return render(request, 'contact.html', {'info': d})

    # CAPTCHA validation
    Captcha_token = request.POST.get("g-recaptcha-response")
    google_api = "https://www.google.com/recaptcha/api/siteverify"
    Captcha_secrete = "6LdG8xoqAAAAAP4IU6KwAJIIuQiuJgiU3BcJiGUB"
    client_data = {"secret": Captcha_secrete, "response": Captcha_token}
    Captcha_Server_response = requests.post(url=google_api, data=client_data)
    Captcha_Server_response_parse = json.loads(Captcha_Server_response.text)
    
    if not Captcha_Server_response_parse.get("success"):
        messages.error(request, "Invalid Captcha, please try again!")
        return render(request, 'contact.html', {'info': d})

    # Prevent header injection by checking for suspicious characters in email headers
    try:
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, 'Message sent successfully!')
    except BadHeaderError:
        messages.error(request, "Invalid header detected. Message not sent.")
        return render(request, 'contact.html', {'info': d})

    return redirect('contact')  # Redirect to the contact page or another page of your choice
