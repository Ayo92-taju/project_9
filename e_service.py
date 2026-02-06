class Customer:
    def __init__(self, name):
        self.name = name
        self.id = 0
        
    def generate_id(self):
        id += 1
        return id
    
    def ask_name(slef):
        name = input("\nEnter name: ")
        return name
    
    def view_customers(self):
        print(f"{self.id}. {self.name}")
        
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.id = 0
        
    def generate_id(self):
        id += 1
        return id
        
    def name_product(self):
        name = input("Enter product name: ")
        return name
    
    def price_tag(self):
        try:
            price = float(input("Enter price: "))
            return price
        
        except ValueError:
                print("Please enter a whole or decimal value")
                
class Cart_item():
    def __init__(self):
        
        self.product = Product()
        self.qty = 0
        
    def select_prod(self):
        try:
            product = int(input("Enter product ID to add product: "))
            return product
        
        except ValueError:
                print("Please enter a whole value")
    
    def ask_qty(self):
        try:
            qty = int(input(f"How many {self.product.name}?: "))
            return qty
        
        except ValueError:
                print("Please enter a whole value")
                
class Cart():
    def __init__(self):
        self.customer = Customer()
        self.item = Cart_item()
        self.shop_cart = []
        
    def add_to_cart(self):
        self.shop_cart.append(self.item)
    