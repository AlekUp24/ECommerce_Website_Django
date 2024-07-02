class Cart():
    def __init__(self,request):

        self.session = request.session

        # get curr sess key
        cart = self.session.get('session_key')

        # if the user is new
        if 'key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages

        self.cart = cart


    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                }
        self.session.modified = True