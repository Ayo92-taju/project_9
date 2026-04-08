from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from e_service import Customer, Product, Cart_item, Cart, Order, Payment
import sqlite3

app = Flask(__name__)

customers = []
products = []
orders = []

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products', methods=['GET'])
def get_products():
    return render_template('products.html', products=products)

@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    product = Product(name, price)
    products.append(product)
    return redirect(url_for('get_products'))

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        return "Product not found."
    products.remove(product)
    return redirect(url_for('get_products'))


@app.route('/customers', methods=['GET'])
def get_customers():
    return render_template('customers.html', customers=customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    customer = Customer(name)
    customers.append(customer)
    return redirect(url_for('get_customers'))

@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    global customers
    customer = next((c for c in customers if c.id == customer_id), None)
    if customer is None:
        return "Customer not found."
    customers.remove(customer)
    return redirect(url_for('get_customers'))


@app.route('/orders', methods=['GET'])
def get_orders():
    return render_template('orders.html', orders=orders, products=products, customers=customers)

@app.route('/orders', methods=['POST'])
def add_order():
    customer_id = request.form['customer_id']
    customer = next((c for c in customers if c.id == int(customer_id)), None)
    if customer is None:
        return "Customer not found."

    product_ids = request.form.getlist('product_id')
    qtys = request.form.getlist('qty')

    cart = Cart(customer)

    for product_id, qty in zip(product_ids, qtys):
        product = next((p for p in products if p.id == int(product_id)), None)
        if product is None:
            continue
        cart_item = Cart_item(product, int(qty))
        cart.add_to_cart(cart_item)

    order = Order(customer, cart)
    orders.append(order)
    return redirect(url_for('get_orders'))

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    global orders
    order = next((o for o in orders if o.id == order_id), None)
    if order is None:
        return "Order not found."
    orders.remove(order)
    return redirect(url_for('get_orders'))


if __name__ == '__main__':
    app.run(debug=True)