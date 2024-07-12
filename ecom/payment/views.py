from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.auth.models import User

# Create your views here.

def payment_success(request):
    return render(request, 'payment/payment_success.html',{})


def checkout(request):


    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, 'payment/checkout.html',{
        'cart_products' : cart_products,
        'quantities'    : quantities,
        'totals'        : totals,
        'shipping_form' : shipping_form,
        })
    
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')