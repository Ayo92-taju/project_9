class Customer:
    _count = 0
    def __init__(self, name):
        self.name = name
        Customer._count += 1
        self.id = Customer._count
        
class Product:
    _count = 0
    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product._count += 1
        self.id = Product._count
                
class Cart_item():
    def __init__(self, product, qty):
        self.product = product
        self.qty = qty
        
    def subtotal(self):
        return self.product.price * self.qty
                
class Cart():
    def __init__(self, customer):
        self.customer = customer
        self.shop_cart = []
        
    def add_to_cart(self, cart_item):
        self.shop_cart.append(cart_item)
    
    def cart_total(self):
        total = 0
        for cart_item in self.shop_cart:
            total += cart_item.subtotal()
        return total
    
class Order():
    _count = 0
    def __init__(self, customer, cart):
        self.customer = customer
        self.cart = cart
        Order._count += 1
        self.id = Order._count
        
class Payment():
    def __init__(self, order):
        self.order = order
        
    def process(self):
        print(f"Payment Confirmed! \n Order #{self.order.id} for {self.order.customer.name} \n Total - ${self.order.cart.cart_total():.2f}")