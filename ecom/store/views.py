from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from cart.cart import Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json


# Create your views here.

def home(request):

    products = Product.objects.all()
    categories= Category.objects.all()
    
    return render(request, 'home.html', {
        'products' : products,
        'categories' : categories}
        )

def about(request):

    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # get old cart
            curr_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = curr_user.old_cart
            if saved_cart:
                # convert to dict using JSON
                converted_cart = json.loads(saved_cart)
                # add cart to curr session
                cart = Cart(request)
                # loop cart and add items from DB
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)


            messages.success(request,("You have been logged in!"))
            return redirect('home')
        else:
            messages.error(request,("There was an error, please try again..."))
            return redirect('login')
    else:   
        return render(request, 'login.html',{})

def logout_user(request):
    
    logout(request)
    messages.success(request,("You have been logged out..."))

    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("You have been registered successfuly! Enjoy!"))
            return redirect('home')
        else:
            messages.error(request,("Oops! There was a problem, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html',{
            'form':form
            })
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request,"User has been updated!")
            return redirect('home')
        else:
            return render(request, 'update_user.html', {"user_form" : user_form})
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid()or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,"User billing info has been updated!")
            return redirect('update_user')
        else:
            return render(request, 'update_info.html', {"form" : form, "shipping_form" : shipping_form })
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password has been updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)

    return render(request, 'product.html',{
        'product':product
        })

def category(request, cat_name):
    cat_name = cat_name.replace('-', ' ')
    categories= Category.objects.all()
    
    if cat_name != 'Sale':
        try:
            category = Category.objects.get(name=cat_name)
            products = Product.objects.filter(category=category)

            return render(request, 'category.html', {
                'products': products,
                'category': category,
                'categories' : categories,
                })
        
        except:
            messages.error(request,("That category doesn't exist!"))
            return redirect('home')
    else:
        try:
            category = 'Currently on Sale!'
            products = Product.objects.filter(is_sale=True)

            return render(request, 'category.html', {
                'products': products,
                'category': category,
                'categories' : categories,
                })
        
        except:
            messages.error(request,("That category doesn't exist!"))
            return redirect('home')
        
def category_summary(request):

    categories = Category.objects.all()

    return render(request, 'category_summary.html', {'categories': categories})


def search(request):
    if request.method == 'POST':
        keyword = request.POST['searched']
        try:
            desc_serch = request.POST['search-description']
        except:
            desc_serch = False
        
        if desc_serch :
            products = Product.objects.filter(Q(name__icontains = keyword) | Q(description__icontains = keyword) )
        else:
            products = Product.objects.filter(name__icontains = keyword)

        return render(request, 'search.html', {'products':products, 'keyword':keyword})
    
    else:
        products = Product.objects.all()
        keyword = ""

        return render(request, 'search.html', {'products':products, 'keyword':keyword})