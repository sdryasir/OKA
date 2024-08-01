from django.shortcuts import render
from products.models import Products
from categories.models import Category
from carousel.models import Carousel

def home(request):
    productdata = Products.objects.all()
    categorydata = Category.objects.all()
    carouseldata = Carousel.objects.all()

    data = {
        'products' : productdata,
        'categories' : categorydata,
        'carousels' : carouseldata
    }
    return render(request, "index.html" , data)


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")

def productDetails(request):
    return render(request, "productdetail.html")

def fashion(request):
    productdata = Products.objects.all()
    data = {
        'products' : productdata,
        }

    return render(request, "products.html" , data)

def searchResult(request):
    return render(request, "search_results.html")

def productResult(request):
    return render(request, "product_results.html")
