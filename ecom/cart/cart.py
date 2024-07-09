from store.models import Product, Profile

class Cart():
    def __init__(self,request):
        self.session = request.session
        self.request = request
        # get curr sess key
        cart = self.session.get('session_key')

        # if the user is new
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages
        self.cart = cart
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id = self.request.user.id)
            # convert single quotations to double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # save carty to profile model
            curr_user.update(old_cart = carty)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id = self.request.user.id)
            # convert single quotations to double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # save carty to profile model
            curr_user.update(old_cart = carty)

    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[str(product_id)]
        else:
            pass

        self.session.modified = True
        
        # remove from old_cart
        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id = self.request.user.id)
            # convert single quotations to double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # save carty to profile model
            curr_user.update(old_cart = carty)

        thing = self.cart
            
        return thing


    def __len__(self):
        return len(self.cart)
    

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)

        return products
    
    
    def get_quantities(self):
        quantities = self.cart

        return quantities
    
    def update(self, product_id, quantity):
        product_id = str(product_id)
        product_qty = int(quantity)

        our_cart = self.cart
        our_cart[product_id] = product_qty

        self.session.modified = True

        # update old_cart
        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id = self.request.user.id)
            # convert single quotations to double
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # save carty to profile model
            curr_user.update(old_cart = carty)

        thing = self.cart

        return thing
    
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        quantities = self.cart

        total = 0

        for key,value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * int(value))
                    else:
                        total = total + (product.price * int(value))
        return total


