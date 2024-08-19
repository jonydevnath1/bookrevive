from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingFrom
from payment.models import ShippingAddress, Order, OrderItem
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] 
        password = request.POST['user_psw'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # shopping cart persistence
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get the save cart from the database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the card
                cart = Cart(request)
                # Loop through the cart and the items from database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You have been login!"))
            
            if user.is_superuser:
                return render(request, 'payment/dashboard.html', {})
            else:
                return redirect('home')
        else:
            messages.error(request, ("There was an error, please try again..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been log out..."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log In user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have register successfully!! Please fill your billing address!!"))
            return redirect('update_info')
        else:
            messages.error(request, ("There is a problem registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'products':product})

def category(request, foo):
    # Replace Hyphens with Space
    foo = foo.replace('_', ' ')
    # Grab the category from the url
    try:
        # Look Up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except Category.DoesNotExist:
        messages.error(request, "That Category Doesn't Exist...")
        return redirect('home')
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('update_user')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You must be login to access this page!!")
        return redirect('home')
    
def update_admin(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('update_admin')
        return render(request, 'update_admin.html', {'user_form': user_form})
    else:
        messages.error(request, "You must be login to access this page!!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            # Do Stuff
            psw_form = ChangePasswordForm(current_user, request.POST)
            if psw_form.is_valid():
                psw_form.save()
                messages.success(request, "You password have been updated!!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(psw_form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            psw_form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'psw_form': psw_form})
    else:
        messages.error(request, "You must be login to access this page!!")
        return redirect('home')
    

def update_admin_pwd(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            # Do Stuff
            psw_form = ChangePasswordForm(current_user, request.POST)
            if psw_form.is_valid():
                psw_form.save()
                messages.success(request, "You password have been updated!!")
                login(request, current_user)
                return redirect('update_admin')
            else:
                for error in list(psw_form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_admin_pwd')
        else:
            psw_form = ChangePasswordForm(current_user)
            return render(request, 'update_admin_pwd.html', {'psw_form': psw_form})
    else:
        messages.error(request, "You must be login to access this page!!")
        return redirect('home')

    
def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get orginal user form
        info_form = UserInfoForm(request.POST or None, instance=current_user)
        # Get orginal user's shipping form
        shipping_form = ShippingFrom(request.POST or None, instance=shipping_user)

        if info_form.is_valid() or shipping_form.is_valid():
            # Save orginal form
            info_form.save()
            # save shipping form
            shipping_form.save()
            
            messages.success(request, "Your Information Has Been Updated!!")
            return redirect('update_info')
        return render(request, 'update_info.html', {'info_form': info_form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "You must be login to access this page!!")
        return redirect('home')
    
def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the Product DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "The product is not found!!")
            return render(request, 'search.html', {})
        else:    
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

def orders(request):
    if request.user.is_authenticated:
        # Get Current User's Profile
        current_user = Profile.objects.get(user__id=request.user.id)
        
        # Fetch Orders associated with the current user
        user_orders = Order.objects.filter(user=current_user.user)
        
        # Fetch all order items for these orders, including product details
        order_items = OrderItem.objects.filter(order__in=user_orders).select_related('product')

        return render(request, 'orders.html', {'orders': user_orders, 'order_items': order_items})
    else:
        return redirect('login')
