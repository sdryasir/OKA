from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")

def login_User(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print('fail')
            return redirect('signup')
    else:
            return render(request, "login.html")
    

def signup(request):
    return render(request, "signup.html")


def productDetails(request):
    return render(request, "productdetail.html")


def fashion(request):
    return render(request, "fashion.html")


def searchResult(request):
    return render(request, "fashion.html")


def register_user(request):
    first_name = request.POST["first_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    if not username or not first_name or not email or not password:
        messages.error(request, "Please Fill All The Fields Correctly!")
        return render(request, "signup.html")
    else:
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Register")
            return render(request, "signup.html")
        elif User.objects.filter(email=email).exists():
            print("email reg")
            messages.error(request, "Email Already Register")
            return render(request, "signup.html")
        else:
            user = User.objects.create_user(
                first_name=first_name, username=username, email=email, password=password
            )
        messages.success(request, "Account created successfully!")
    return render(request, "signup.html")
