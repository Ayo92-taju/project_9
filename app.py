from flask import Flask, request

from e_service import Customer, Product, Cart_item, Cart, Order, Payment

app = Flask(__name__)

# In-memory storage
customers = []
products = []
orders = []


@app.route('/products', methods=['GET'])
def get_products():
    if not products:
        return "No products available."
    result = ""
    for p in products:
        result += f"{p.id}. {p.name} — ${p.price:.2f}\n"
    return result

@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    product = Product(name, price)
    products.append(product)
    return f"Product '{product.name}' added with ID {product.id}."


@app.route('/customers', methods=['GET'])
def get_customers():
    if not customers:
        return "No customers available."
    result = ""
    for c in customers:
        result += f"{c.id}. {c.name}\n"
    return result

@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    customer = Customer(name)
    customers.append(customer)
    return f"New customer '{customer.name}' added with ID {customer.id}."


if __name__ == '__main__':
    app.run(debug=True)