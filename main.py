from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

@app.route('/')
def home():
    try:
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []

    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form.get('category')
        new_category = request.form.get('new_category')

        # تحديد التصنيف النهائي
        final_category = new_category if new_category else category

        product = {
            'name': name,
            'price': price,
            'category': final_category
        }

        try:
            with open(DATA_FILE, 'r') as f:
                products = json.load(f)
        except FileNotFoundError:
            products = []

        products.append(product)

        with open(DATA_FILE, 'w') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        return redirect(url_for('admin'))

    try:
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []

    # استخراج التصنيفات
    categories = list(set([p['category'] for p in products if 'category' in p]))

    return render_template('admin.html', categories=categories)

@app.route('/products')
def view_products():
    try:
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []

    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
