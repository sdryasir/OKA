from django.shortcuts import render
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from smtplib import SMTPException
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
from orders.models import Orders , OrderItem


stripe.api_key = 'sk_test_51PnwfEG84wrz8yN3pN99IhWeXEqKCsXVeSoLT4n7fIlm7AXOFVXMI2B4nxmkJgsuVeLVnvZFY6TogGyCPlGMxkzq00T1b1FcpY'

def header(request):
    header = Header.objects.all()
    footer = Footer.objects.all()
    print(header)
    print(footer)
    data = {
        "footer": footer,
        "header": header,
    }
    return render(request, "header.html", data)

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
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email is already in use.')
            else:
                user = form.save()
                return redirect("login")
    else:
        form = CustomUserForm()
    
    return render(request, "signup.html", {"form": form})


def productDetails(request, id):
    productsdetails = Products.objects.get(id__exact=id)

    data = {
        "products": productsdetails,
    }

    return render(request, "productdetail.html", data)


def products(request):
    sort_order = request.GET.get("sort_order")
    minprice = request.GET.get("min_price", 0)
    maxprice = request.GET.get("max_price", 5000)
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
        search_results = search_results.filter(price__gte=min_price, price__lte=max_price)

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

    # Prepare context data for rendering the template
    context = {
        "searchterm": search_results,
        "search_query": search_term,  # Pass the search term to the template
        "sort_order": sort_order,
        "minprice": min_price,
        "maxprice": max_price
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
        return render(request, "product_results.html")

    paginator = Paginator(productsbycat, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    totalpage = [x + 1 for x in range(paginator.num_pages)]

    data = {
        "products": page_obj,
        "totalpages": totalpage,
        "productsbycat": productsbycat,
        "sort_order": sort_order,
        "minprice": min_price,
        "maxprice": max_price,
        "category": category,
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
    data = {"faq": faq}
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

    session_cart = cart.session.get('cart', {})

    if isinstance(session_cart, dict) and session_cart:
        for item in session_cart.values():
            try:
                price = int(item["price"])
                quantity = int(item["quantity"])
                subtotal += price * quantity

                # Add each product as a line item
                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item["name"],  # Product name from cart
                        },
                        "unit_amount": price * 100,  # Convert dollars to cents
                    },
                    "quantity": quantity,  # Dynamic quantity
                })
            except (ValueError, KeyError) as e:
                print(f"Error processing item: {e}")

        total = subtotal + 200  # Calculate the total

        # Store total and line items in session
        request.session['total'] = total
        request.session['line_items'] = line_items

    data = {
        "subtotal": subtotal,
        "total": total
    }

    return render(request, "cart_detail.html", data)


def create_checkout_session(request):
    cart = Cart(request)
    subtotal = 0
    shipping_fee = 200 * 100  # Shipping fee in cents (200 PKR)
    total = 0

    # Initialize a list to store line items for Stripe
    line_items = []

    session_cart = cart.session.get('cart', {})

    if isinstance(session_cart, dict) and session_cart:
        for item in session_cart.values():
            try:
                price = int(item["price"]) * 100  # Convert PKR to cents
                quantity = int(item["quantity"])
                subtotal += price * quantity

                # Add each product as a line item
                line_items.append({
                    "price_data": {
                        "currency": "pkr",
                        "product_data": {
                            "name": item["name"],  # Product name from cart
                        },
                        "unit_amount": price,  # Price in cents
                    },
                    "quantity": quantity,  # Dynamic quantity
                })
            except (ValueError, KeyError) as e:
                print(f"Error processing item: {e}")

        total = subtotal + shipping_fee  # Calculate the total

        # Store total and line items in session
        request.session['total'] = total
        request.session['line_items'] = line_items
    total = request.session.get('total', 0)
    line_items = request.session.get('line_items', [])

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,  # Use the dynamic line items
            mode="payment",
            success_url=settings.YOUR_DOMAIN + "success",
            cancel_url=settings.YOUR_DOMAIN + "cancel",
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
        if checkout_session:
            order = Orders.objects.create(
                user=request.user,
                total_price=total / 100,  # Convert cents back to PKR
                payment_id=checkout_session.id,
                payment_status="unpaid"
            )
            if order:
                for item in session_cart.values():
                    OrderItem.objects.create(
                        order=order,
                        product_name=item["name"],
                        quantity=item["quantity"],
                        price=item["price"]
                    )
    except Exception as e:
        print('==================================')
        print(e)
        print('+++++++++++++++++++++++++++++++++++')

    return redirect(checkout_session.url, code=303)





def success(request):
    session_id = request.GET.get('session_id')

    if session_id:
        try:
            # Find the order associated with this session_id
            order = Orders.objects.get(payment_id=session_id)

            # Check if the payment status is 'paid'
            if order.payment_status == 'paid':
                # Clear the cart
                cart = Cart(request)
                cart.clear()

                # Send confirmation email
                send_confirmation_email(order)

                # Render the success template
                return render(request, 'success.html', {'order': order})

            return HttpResponse("Payment was not successful.")

        except Orders.DoesNotExist:
            return HttpResponse("Order not found.")

    return HttpResponse("Session ID not provided.")


def send_confirmation_email(order):
    subject = 'Order Confirmation'
    message = f"""
    Dear {order.user.username},

    Thank you for your purchase!

    Your order has been successfully processed. 
    Order ID: {order.id}
    Total Amount: {order.total_price} PKR

    We appreciate your business and hope to serve you again soon.

    Best regards,
    Your Company Name
    """
    recipient_list = [order.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def cancel(request):
    return render(request, "cancel.html")
