from store.models import Product 

class Cart():
    def __init__(self,request):

        self.session = request.session

        # get curr sess key
        cart = self.session.get('session_key')

        # if the user is new
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages

        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = str(product_qty)

        self.session.modified = True

    def delete(self):
        
       pass


    def __len__(self):
        return len(self.cart)
    

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)

        return products
    
    def get_quantities(self):
        
        quantities = self.cart

        return quantities