from shophouse.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart =self.session.get('session_key')

        # If there is no session yet, create a new  one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
       
        #  make sure cart is available on all pages of the site
        self.cart = cart

    def add(self, product):
        """
        Add a product to the cart
        """
        product_id = str(product.id)

        # If the product is already in the cart, update the quantity
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = self.cart[product_id].get('quantity', 0) + 1
        # If the product is not in the cart, add it
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': 1,
                'name': product.name,
                'image': product.image.url if product.image else None
            }
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

    def update(self, product, quantity):
        """
        Update the quantity of a product in the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity

    def clear(self):
        """
        Clear the cart
        """
        self.session['session_key'] = {}

    def get_total_price(self):
        """
        Get the total price of all products in the cart
        """
        total_price = 0
        for item in self.cart.values():
            total_price += float(item['price']) * item['quantity']
        return total_price

    def get_prods(self):
        product_Ids =self.cart.keys()
        products = Product.objects.filter(id__in=product_Ids)
        return products
    
        
    
    def __len__(self):
        return len(self.cart)

