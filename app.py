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