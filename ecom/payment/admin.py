from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# TO SEE ORDER ITEMS UNDER ORDER IN ADMIN VIEW

# create order item inline

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend order model

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]


# re-register Order AND Order Admin
admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)