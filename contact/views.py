from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from .models import Contact, Usrinfo

def contact(request):
    info = Usrinfo.objects.all()
    print(info)
    data ={
        "info": info
    }
    return render(request, 'contact.html', data)

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
        Captcha_token = request.POST["g-recaptcha-response"]
        google_api = "https://www.google.com/recaptcha/api/siteverify"
        Captcha_secrete = "6LdG8xoqAAAAAP4IU6KwAJIIuQiuJgiU3BcJiGUB"
        client_data = {"secret": Captcha_secrete, "response": Captcha_token}
        Captcha_Server_response = requests.post(
                    url=google_api, data=client_data
                )
        Captcha_Server_response_parse = json.loads(Captcha_Server_response.text)
        if Captcha_Server_response_parse["success"] == False:
            messages.error(request, "Invalid Captcha Try Again!")
            return redirect("login")
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, 'Sent Successfully!')
        return redirect('contact')  # Redirect to the contact page or another page of your choice
