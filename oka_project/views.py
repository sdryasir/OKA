from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
import logging
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from smtplib import SMTPException
from reviews.models import Reviews
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
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
import stripe
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from offer.models import Offer
from cart.cart import Cart
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserForm
from django.contrib import messages
from django.http import JsonResponse
from header_footer.models import Header
from header_footer.models import Footer
from orders.models import Orders, OrderItem
from users.models import Userdata


stripe.api_key = "sk_test_51PnwfEG84wrz8yN3pN99IhWeXEqKCsXVeSoLT4n7fIlm7AXOFVXMI2B4nxmkJgsuVeLVnvZFY6TogGyCPlGMxkzq00T1b1FcpY"


def header(request):
    header = Header.objects.all()
    footer = Footer.objects.all()

    data = {
        "footer": footer,
        "header": header,
    }
    return render(request, "header.html", data)

def home(request):
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    productdata = list(Products.objects.all())
    categorydata = list(Category.objects.all())
    carouseldata = list(Carousel.objects.all())
    offerdata = list(Offer.objects.all())
    random.shuffle(productdata)
    random.shuffle(categorydata)
    random.shuffle(carouseldata)
    random.shuffle(offerdata)

    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None

        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('home')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    data = {
        "products": productdata,
        "categories": categorydata,
        "carousels": carouseldata,
        "offer": offerdata,
        "profile_picture": profile_picture,
        "city": city,
        "country": country,
        "address": address,
        "phone_no": phone_no,
        }
    return render(request, "index.html", data)

def contact(request):
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('contact')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    return render(request, "contact.html"    ,{"profile_picture": profile_picture,"city": city,"country": country,"address": address,"phone_no": phone_no})


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

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Email is already in use.")
            else:
                user = form.save()
                return redirect("login")
    else:
        form = CustomUserForm()

    return render(request, "signup.html", {"form": form})


def product_details(request, id):
    productsdetails = Products.objects.get(id__exact=id)
    reviews = Reviews.objects.filter(Item=id).order_by('-id')
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('productDetails', id)
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    data = {
        "products": productsdetails,
        "profile_picture": profile_picture,
        "city": city,
        "country": country,
        "address": address,
        "phone_no": phone_no,
        "reviews":reviews
    }

    return render(request, "productdetail.html", data)


def products(request):
    # Retrieve query parameters for sorting and filtering
    sort_order = request.GET.get("sort_order")
    minprice = request.GET.get("min_price", 0)
    maxprice = request.GET.get("max_price", 5000)
    
    # Get all product data
    productdata = Products.objects.all()
    
    # Apply price filtering
    if minprice or maxprice:
        productdata = productdata.filter(price__gte=minprice, price__lte=maxprice)
    
    # Apply sorting based on the sort_order parameter
    if sort_order == "ascending":
        productdata = productdata.order_by("price")
    elif sort_order == "descending":
        productdata = productdata.order_by("-price")
    elif sort_order == "lth":
        productdata = productdata.order_by("price")
    elif sort_order == "htl":
        productdata = productdata.order_by("-price")
    else:
        # Random shuffle if no sorting is applied
        productdata = list(productdata)
        random.shuffle(productdata)

    # Paginate the product data (8 products per page)
    paginator = Paginator(productdata, 8)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    
    # List total pages for pagination
    totalpage = [x + 1 for x in range(paginator.num_pages)]
    
    # Handle authenticated user profile data
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST' and 'profile_picture' in request.FILES:
            # Save the profile picture
            userdata.profile_picture = request.FILES['profile_picture']
            userdata.save()
            return redirect('products')
        
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    # Pass data to the template
    data = {
        "products": page_obj,
        "totalpages": totalpage,
        "sort_order": sort_order,
        "minprice": minprice,
        "maxprice": maxprice,
        "profile_picture": profile_picture,
        "city": city,
        "country": country,
        "address": address,
        "phone_no": phone_no
    }

    return render(request, "products.html", data)


def resetfilter(request):
    return render(request, "products.html")


def searchResult(request):
    # Get search term and filter parameters from the request
    search_term = request.GET.get("search", "")
    sort_order = request.GET.get("sort_order")
    min_price = request.GET.get("min_price", 0)
    max_price = request.GET.get("max_price", 5000)

    # Start with a base queryset that includes the search term
    search_results = Products.objects.filter(name__icontains=search_term)

    # Apply price filter if min_price or max_price is specified
    if min_price or max_price:
        search_results = search_results.filter(
            price__gte=min_price, price__lte=max_price
        )

    # Apply sorting if sort_order is specified
    if sort_order == "ascending":
        search_results = search_results.order_by("price")
    elif sort_order == "descending":
        search_results = search_results.order_by("-price")
    elif sort_order == "lth":
        search_results = search_results.order_by("price")
    elif sort_order == "htl":
        search_results = search_results.order_by("-price")

    # Check if there are any results and handle the case where no products are found
    if not search_results.exists():
        messages.error(request, "No Product Found!")
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('products')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    # Prepare context data for rendering the template
    context = {
        "searchterm": search_results,
        "search_query": search_term,  # Pass the search term to the template
        "sort_order": sort_order,
        "minprice": min_price,
        "maxprice": max_price,
        "profile_picture": profile_picture,
        "city": city,
        "country": country,
        "address": address,
        "phone_no": phone_no
    }

    return render(request, "search_results.html", context)


def productResult(request, category):
    productsbycat = Products.objects.filter(category_id=category)

    # Retrieve filter parameters
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort_order = request.GET.get("sort_order")

    # Apply price range filter
    if min_price and max_price:
        productsbycat = productsbycat.filter(price__gte=min_price, price__lte=max_price)

    # Apply sorting
    if sort_order == "ascending":
        productsbycat = productsbycat.order_by("price")
    elif sort_order == "descending":
        productsbycat = productsbycat.order_by("-price")
    elif sort_order == "lth":
        productsbycat = productsbycat.order_by("price")
    elif sort_order == "htl":
        productsbycat = productsbycat.order_by("-price")
    else:
        productsbycat = list(productsbycat)
        random.shuffle(productsbycat)

    # Handle no products case
    if not productsbycat:
        messages.error(request, "No Product Found!")
        return render(request, "product_results.html", {"category": category})

    paginator = Paginator(productsbycat, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    totalpage = [x + 1 for x in range(paginator.num_pages)]
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('product-results', category=category)
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    data = {
        "products": page_obj,
        "totalpages": totalpage,
        "productsbycat": productsbycat,
        "sort_order": sort_order,
        "minprice": min_price,
        "maxprice": max_price,
        "category": category,
        "profile_picture": profile_picture,
        "city": city,
        "country": country,
        "address": address,
        "phone_no": phone_no
    }

    return render(request, "product_results.html", data)

# def register_user(request):
#     if not request.user.is_authenticated:
#         first_name = request.POST["first_name"]
#         username = request.POST["username"]
#         email = request.POST["email"]
#         password = request.POST["password"]
#         if not username or not first_name or not email or not password:
#             messages.error(request, "Please Fill All The Fields Correctly!")
#             return render(request, "signup.html")
#         else:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username Already Register")
#                 return render(request, "signup.html")
#             elif User.objects.filter(email=email).exists():
#                 messages.error(request, "Email Already Register!")
#                 return render(request, "signup.html")
#             elif len(password) < 8:
#                 messages.error(request, "Password Must be 8 Characters Long!")
#                 return render(request, "signup.html")
#             else:
#                 user = User.objects.create_user(
#                     first_name=first_name,
#                     username=username,
#                     email=email,
#                     password=password,
#                 )
#                 try:
#                     validate_email(email)
#                     email_msg = EmailMessage(
#                         f"Welcome! {first_name}",
#                         "<h1>Welcome To Baby Planet Thankx For Account Creation!</h1>",
#                         "info@nullxcoder.xyz",
#                         to=[email],
#                     )
#                     email_msg.content_subtype = "html"  # Set the email content to HTML
#                     email_msg.send()
#                 except ValidationError:
#                     return HttpResponse("Invalid email address.")
#                 except BadHeaderError:
#                     return HttpResponse("Invalid header found.")
#                 except SMTPException:
#                     return HttpResponse("There was an error sending the email.")
#                 Captcha_token = request.POST["g-recaptcha-response"]
#                 google_api = "https://www.google.com/recaptcha/api/siteverify"
#                 Captcha_secrete = "6LdG8xoqAAAAAP4IU6KwAJIIuQiuJgiU3BcJiGUB"
#                 client_data = {"secret": Captcha_secrete, "response": Captcha_token}
#                 Captcha_Server_response = requests.post(
#                     url=google_api, data=client_data
#                 )
#                 Captcha_Server_response_parse = json.loads(Captcha_Server_response.text)
#                 if Captcha_Server_response_parse["success"] == False:
#                     messages.error(request, "Invalid Captcha Try Again!")
#                     return render(request, "signup.html")
#                 else:
#                     messages.success(request, "Account created successfully!")
#                     return render(request, "login.html")
#     else:
#         return redirect("home")


# def checkout(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             print('jvchdchajdchvjhcvaj' , user)
#         else:
#             print('hgjsjghcdddddddddghchcgchjchjchch')
#     else:

#         form = CustomUserForm()
#     return render(request, "checkout.html", {"form": form})


def faq(request):
    faq = Faq.objects.all()
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('faq')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None
    data = {"faq": faq , "profile_picture": profile_picture , "city": city , "country": country , "address": address , "phone_no": phone_no}
    return render(request, "faq.html", data)


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    cart = Cart(request)
    subtotal = 0
    total = 0

    # Initialize a list to store line items for Stripe
    line_items = []

    session_cart = cart.session.get("cart", {})

    if isinstance(session_cart, dict) and session_cart:
        for item in session_cart.values():
            try:
                price = int(item["price"])
                quantity = int(item["quantity"])
                subtotal += price * quantity

                # Add each product as a line item
                line_items.append(
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": item["name"],  # Product name from cart
                            },
                            "unit_amount": price * 100,  # Convert dollars to cents
                        },
                        "quantity": quantity,  # Dynamic quantity
                    }
                )
            except (ValueError, KeyError) as e:
                print(f"Error processing item: {e}")

        total = subtotal + 200  # Calculate the total

        # Store total and line items in session
        request.session["total"] = total
        request.session["line_items"] = line_items
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('cart_detail')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None

    data = {"subtotal": subtotal, "total": total , "profile_picture": profile_picture , "city": city , "country": country , "address": address , "phone_no": phone_no}

    return render(request, "cart_detail.html", data)




def create_checkout_session(request):
    cart = Cart(request)
    subtotal = 0
    shipping_fee = 200 * 100  # Shipping fee in cents (200 PKR)
    total = 0

    line_items = []
    session_cart = cart.session.get("cart", {})

    if isinstance(session_cart, dict) and session_cart:
        for item in session_cart.values():
            try:
                price = int(item["price"]) * 100  # Convert PKR to cents
                quantity = int(item["quantity"])
                subtotal += price * quantity

                # Add each product as a line item for Stripe
                line_items.append(
                    {
                        "price_data": {
                            "currency": "pkr",
                            "product_data": {
                                "name": item["name"],
                            },
                            "unit_amount": price,
                        },
                        "quantity": quantity,
                    }
                )
            except (ValueError, KeyError) as e:
                print(f"Error processing item: {e}")

        total = subtotal + shipping_fee

    # Create an order in your system
    order = Orders.objects.create(
        user=request.user,
        total_price=total / 100,  # Convert cents back to PKR
        payment_status="unpaid",
    )

    # Create a Stripe checkout session with client_reference_id as the order ID
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        success_url=settings.YOUR_DOMAIN + "success",
        cancel_url=settings.YOUR_DOMAIN + "cancel",
        client_reference_id=order.id,  # Pass the order ID for matching in webhook
        shipping_options=[
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {
                        "amount": shipping_fee,
                        "currency": "pkr",
                    },
                    "display_name": "Standard Shipping",
                    "delivery_estimate": {
                        "minimum": {"unit": "business_day", "value": "5"},
                        "maximum": {"unit": "business_day", "value": "7"},
                    },
                }
            }
        ],
    )

    return redirect(checkout_session.url, code=303)

def success(request):
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('home')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None
    return render(request, "success.html" , {"profile_picture": profile_picture , "city": city , "country": country , "address": address , "phone_no": phone_no})

def cancel(request):
    profile_picture = None
    city = None
    country = None
    address = None
    phone_no = None
    if request.user.is_authenticated:
        userdata, created = Userdata.objects.get_or_create(user=request.user)
        profile_picture = userdata.profile_picture.url if userdata.profile_picture else None
    
        if request.method == 'POST':
            if 'profile_picture' in request.FILES:
                # Save the profile picture
                userdata.profile_picture = request.FILES['profile_picture']
                userdata.save()
                return redirect('home')
        city = userdata.city if userdata.city else None
        country = userdata.country if userdata.country else None
        address = userdata.address if userdata.address else None
        phone_no = userdata.phone_no if userdata.phone_no else None
    
    return render(request, "cancel.html" , {"profile_picture": profile_picture , "city": city , "country": country , "address": address , "phone_no": phone_no})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        print(f"Received event: {json.dumps(event, indent=2)}")  # Log the entire event payload
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id')
        client_reference_id = session.get('client_reference_id')  # Retrieve the order ID
        print(f"Processing checkout.session.completed for session_id: {session_id}, client_reference_id: {client_reference_id}")

        try:
            # Fetch the order using client_reference_id
            order = Orders.objects.get(id=client_reference_id)
            order.payment_status = "paid"
            order.payment_id = session_id  # Optionally store the Stripe session ID
            order.save()
            print(f"Order updated: {order}")
        except Orders.DoesNotExist:
            print(f"Order with client_reference_id {client_reference_id} not found")

    elif event['type'] == 'payment_intent.succeeded':
        # Handle the payment_intent.succeeded event if needed
        print(f"PaymentIntent succeeded: {json.dumps(event, indent=2)}")

    elif event['type'] == 'payment_intent.payment_failed':
        # Handle the payment_intent.payment_failed event if needed
        print(f"PaymentIntent failed: {json.dumps(event, indent=2)}")

    return JsonResponse({'status': 'success'}, status=200)

# Configure logger
logger = logging.getLogger(__name__)
@login_required
def submit_review(request, id):
    referrer = request.META.get('HTTP_REFERER', 'home') 
    product = get_object_or_404(Products, id=id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        opinion = request.POST.get("opinion")

        if not rating or not opinion:
            messages.error(request, "Please fill in both fields!")
            return redirect(referrer)

        existing_review = Reviews.objects.filter(user=request.user, Item=product).first()
        if existing_review:
            messages.error(request, "You have already reviewed this product.")
            return redirect(referrer)

        # Optionally fetch an order item if needed
        order_item = OrderItem.objects.filter(order__user=request.user, product_name=product.name).first()

        try:
            Reviews.objects.create(
                rating=rating,
                opinion=opinion,
                user=request.user,
                Item=product,
                order=order_item.order if order_item else None,  # Assign None if no order_item
            )
            messages.success(request, "Review submitted successfully.")
            return redirect("productdetail", id=id)
        except Exception as e:
            logger.error(f"Error submitting review: {e}")
            return redirect(referrer)

    return render(request, "productdetail.html", {"product": product})