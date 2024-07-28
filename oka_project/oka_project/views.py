from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
def productDetails(request):
    return render(request, "productdetail.html")
