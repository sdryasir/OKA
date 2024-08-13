from django.shortcuts import render
from Product.models import Products
from categories.models import Category
from carousel.models import Carousel
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login as auth_login, logout
from faq.models import Faq
import random
from django.core.paginator import Paginator, EmptyPage
from offer.models import Offer
from cart.cart import Cart
from django.http import HttpResponseRedirect


def home(request):
    productdata = list(Products.objects.all())
    categorydata = list(Category.objects.all())
    carouseldata = list(Carousel.objects.all())
    offerdata = list(Offer.objects.all())
    random.shuffle(productdata)
    random.shuffle(categorydata)
    random.shuffle(carouseldata)
    random.shuffle(offerdata)

    data = {
        "products": productdata,
        "categories": categorydata,
        "carousels": carouseldata,
        "offer": offerdata,
    }
    return render(request, "index.html", data)


def contact(request):
    return render(request, "contact.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, "login.html")


def log_inUser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            if not username or not password:
                messages.error(request, "Please Fill All The Fields!")
                return redirect("login")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, "Login Successful!")
                auth_login(request, user)
                request.session["username"] = user.username
                return redirect("home")
            else:
                messages.error(request, "Login Failed! Cheack Your Credentials!")
                return redirect("login")
        else:
            messages.error(request, "invalid Command")
            return render(request, "login.html")
    else:
        return redirect("home")


def log_out_user(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()
        messages.success(request, "Successfully Logout!")
        return render(request, "login.html")
    else:
        return redirect("login")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, "signup.html")


def productDetails(request, id):
    productsdetails = Products.objects.get(id__exact=id)

    data = {
        "products": productsdetails,
    }

    return render(request, "productdetail.html", data)


def products(request):
    sort_order = request.GET.get("sort_order")
    minprice = request.GET.get("min_price")
    maxprice = request.GET.get("max_price")
    productdata = Products.objects.all()

    if minprice or maxprice:
        productdata = productdata.filter(price__gte=minprice, price__lte=maxprice)

    if sort_order == "ascending":
        productdata = productdata.order_by("price")
    elif sort_order == "descending":
        productdata = productdata.order_by("-price")
    elif sort_order == "lth":
        productdata = productdata.order_by("price")
    elif sort_order == "htl":
        productdata = productdata.order_by("-price")
    else:
        productdata = list(productdata)
        random.shuffle(productdata)

    paginator = Paginator(productdata, 8)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    totalpage = [x + 1 for x in range(paginator.num_pages)]

    data = {
        "products": page_obj,
        "totalpages": totalpage,
        "sort_order": sort_order,
        "minprice": minprice,
        "maxprice": maxprice,
    }

    return render(request, "products.html", data)


def searchResult(request):
    searchresults = request.GET.get('search')
    searchterm = Products.objects.filter(name__icontains=searchresults)
    if not searchterm.exists():
        messages.error(request, "No Product Found!")
        return render(request, "search_results.html")
    data = {"searchterm": searchterm}
    return render(request, "search_results.html", data)


def productResult(request, category):
    productsbycat = Products.objects.filter(category_id=category)
    sort_data = request.GET.get("sort_order")
    if sort_data == "ascending":
        productsbycat = Products.objects.filter(category_id=category).order_by("id")
    elif sort_data == "descending":
        productsbycat = Products.objects.filter(category_id=category).order_by("-id")
    else:
        productsbycat = list(Products.objects.filter(category_id=category))
        random.shuffle(productsbycat)
    if not productsbycat:
        messages.error(request, "No Product Found!")
        return render(request, "product_results.html")
    data = {
        "productsbycat": productsbycat,
        "sort_data": sort_data,
    }

    return render(request, "product_results.html", data)


def register_user(request):
    if not request.user.is_authenticated:
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
                messages.error(request, "Email Already Register!")
                return render(request, "signup.html")
            elif len(password) < 8:
                messages.error(request, "Password Must be 8 Characters Long!")
                return render(request, "signup.html")
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    username=username,
                    email=email,
                    password=password,
                )
                messages.success(request, "Account created successfully!")
        return render(request, "signup.html")
    else:
        return redirect("home")


# Create your views here.


def faq(request):
    faq = Faq.objects.all()
    data = {"faq": faq}
    return render(request, "faq.html", data)


def cart_add(request, id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Products.objects.get(id=id)
        cart.add(product=product)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        cart = Cart(request)
        product = Products.objects.get(id=id)
        cart.add(product=product)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    return render(request, "cart_detail.html")
