from .cart import Cart

# create context processor so out cart works on all pages

def cart(request):
    return {'cart' : Cart(request)}