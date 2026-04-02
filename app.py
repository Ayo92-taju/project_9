from flask import Flask, request

from e_service import Customer, Product, Cart_item, Cart, Order, Payment

app = Flask(__name__)

customers = []
products = []
orders = []


@app.route('/')
def home():
    return '''
    <h2>E-Commerce System</h2>
    <ul>
        <li><a href="/products">Products</a></li>
        <li><a href="/customers">Customers</a></li>
        <li><a href="/orders">Orders</a></li>
    </ul>
    '''


@app.route('/products', methods=['GET'])
def get_products():
    if not products:
        result = "<p>No products available.</p>"
    else:
        result = "<ul>"
        for p in products:
            result += f'''
                <li>
                {p.id}. {p.name} — ${p.price:.2f}
                <form method="POST" action="/products/delete/{p.id}" style="display:inline">
                    <button type="submit">Delete</button>
                </form>
            </li>
            '''
        result += "</ul>"

    return f'''
    <h2>Products</h2>
    {result}
    <h3>Add Product</h3>
    <form method="POST" action="/products">
        <input name="name" placeholder="Product name" required><br><br>
        <input name="price" placeholder="Price" required><br><br>
        <button type="submit">Add Product</button>
    </form>
    <br><a href="/">Back</a>
    '''


@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    product = Product(name, price)
    products.append(product)
    return f'''
    <p>Product <b>{product.name}</b> added with ID {product.id}.</p>
    <a href="/products">Back to products</a>
    '''

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        return "Product not found."
    products.remove(product)
    return f'''
    <p>Product <b>{product.name}</b> deleted.</p>
    <a href="/products">Back to products</a>
    '''


@app.route('/customers', methods=['GET'])
def get_customers():
    if not customers:
        result = "<p>No customers yet.</p>"
    else:
        result = "<ul>"
        for c in customers:
            result += f'''
            <li>
                {c.id}. {c.name}
                <form method="POST" action="/customers/delete/{c.id}" style="display:inline">
                    <button type="submit">Delete</button>
                </form>
            </li>
            '''
        result += "</ul>"

    return f'''
    <h2>Customers</h2>
    {result}
    <h3>Add Customer</h3>
    <form method="POST" action="/customers">
        <input name="name" placeholder="Customer name" required><br><br>
        <button type="submit">Add Customer</button>
    </form>
    <br><a href="/">Back</a>
    '''


@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    customer = Customer(name)
    customers.append(customer)
    return f'''
    <p>Customer <b>{customer.name}</b> added with ID {customer.id}.</p>
    <a href="/customers">Back to customers</a>
    '''

@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    global customers
    customer = next((c for c in customers if c.id == customer_id), None)
    if customer is None:
        return "Customer not found."
    customers.remove(customer)
    return f'''
    <p>Customer <b>{customer.name}</b> deleted.</p>
    <a href="/customers">Back to customers</a>
    '''


@app.route('/orders', methods=['GET'])
def get_orders():
    if not orders:
        result = "<p>No orders yet.</p>"
    else:
        result = "<ul>"
        for o in orders:
            result += f'''
            <li>
            Order #{o.id} — {o.customer.name} — ${o.cart.cart_total():.2f}
            <form method="POST" action="/orders/delete/{o.id}" style="display:inline">
                <button type="submit">Delete</button>
            </form>
            </li>
            '''
        result += "</ul>"

    product_options = "".join(
        f'<option value="{p.id}">{p.name} (${p.price:.2f})</option>'
        for p in products
    )
    customer_options = "".join(
        f'<option value="{c.id}">{c.name}</option>'
        for c in customers
    )

    return f'''
    <h2>Orders</h2>
    {result}
    <h3>Place Order</h3>
    <form method="POST" action="/orders">
        <select name="customer_id">{customer_options}</select><br><br>
        <select name="product_id">{product_options}</select><br><br>
        <input name="qty" placeholder="Quantity" required><br><br>
        <select name="product_id">{product_options}</select><br><br>
        <input name="qty" placeholder="Quantity" required><br><br>
        <button type="submit">Place Order</button>
    </form>
    <br><a href="/">Back</a>
    '''


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

    return f'''
    <p>Order <b>#{order.id}</b> placed for <b>{customer.name}</b> — Total: <b>${cart.cart_total():.2f}</b></p>
    <a href="/orders">Back to orders</a>
    '''

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    global orders
    order = next((o for o in orders if o.id == order_id), None)
    if order is None:
        return "Order not found."
    orders.remove(order)
    return f'''
    <p>Order <b>{order.id}</b> deleted.</p>
    <a href="/orders">Back to orders</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)