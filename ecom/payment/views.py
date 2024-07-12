from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from django.contrib.auth.models import User
from payment.models import ShippingAddress, Order, OrderItem
from store.models import Product
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
    
def billing_info(request):

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        payment_user = ShippingAddress.objects.get(user_id=request.user.id)
        
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        payment_form = PaymentForm()

        return render(request, 'payment/billing_info.html',{
        'cart_products' : cart_products,
        'quantities'    : quantities,
        'totals'        : totals,
        'shipping_form' : shipping_form,
        'payment_form'  : payment_form,
        })
    
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')
    
def process_order(request):
    if request.user.is_authenticated:
        if request.POST:
            payment_form = PaymentForm(request.POST or None)
            # get shipping data
            shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            
            # gather order info
            user = request.user
            shipping_address = f"{shipping_user.shipping_address1}\n{shipping_user.shipping_address2}\n{shipping_user.shipping_city}\n{shipping_user.shipping_state}\n{shipping_user.shipping_zipcode}\n{shipping_user.shipping_country}\n"
            full_name = shipping_user.shipping_full_name
            email = shipping_user.shipping_email
            cart = Cart(request)
            amount_paid = cart.cart_total()

            cart_products = cart.get_products()
            
            # create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # add order items
            order_id = create_order.pk
            quantities = cart.get_quantities()
            for product in cart_products:
                product_id =  product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                

                for key,value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=value, price=price)
                        create_order_item.save()

            messages.success(request,"Order placed successfuly.")
            return redirect('home')
        
        else:
            messages.success(request,"You must be logged in to access that page.")
            return redirect('home')
    else:
        messages.success(request,"You must be logged in to access that page.")
        return redirect('home')