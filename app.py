from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)


@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    conn = get_db()
    conn.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()
    return redirect(url_for('get_products'))


@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_products'))


@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)


@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    conn = get_db()
    conn.execute('INSERT INTO customers (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_customers'))


@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    conn = get_db()
    conn.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_customers'))


@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    orders = conn.execute('''
        SELECT orders.id, customers.name as customer_name,
               SUM(order_items.qty * products.price) as total
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN order_items ON order_items.order_id = orders.id
        JOIN products ON order_items.product_id = products.id
        GROUP BY orders.id
    ''').fetchall()
    products = conn.execute('SELECT * FROM products').fetchall()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders, products=products, customers=customers)


@app.route('/orders', methods=['POST'])
def add_order():
    customer_id = request.form['customer_id']
    product_ids = request.form.getlist('product_id')
    qtys = request.form.getlist('qty')

    conn = get_db()
    cursor = conn.execute('INSERT INTO orders (customer_id) VALUES (?)', (customer_id,))
    order_id = cursor.lastrowid

    for product_id, qty in zip(product_ids, qtys):
        conn.execute('INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)', (order_id, product_id, qty))

    conn.commit()
    conn.close()
    return redirect(url_for('get_orders'))


@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_orders'))


if __name__ == '__main__':
    app.run(debug=True)