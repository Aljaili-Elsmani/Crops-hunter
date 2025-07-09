from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_products():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_products(products):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    products = load_products()
    # تجميع المنتجات حسب التصنيف
    categories = {}
    for p in products:
        cat = p.get('category', 'غير مصنف')
        categories.setdefault(cat, []).append(p)
    return render_template('index.html', categories=categories)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']  # وحدة القياس مثلا: جرام، طن
        category = request.form.get('category')
        new_category = request.form.get('new_category')

        final_category = new_category.strip() if new_category else category

        product = {
            'name': name,
            'price': price,
            'unit': unit,
            'category': final_category
        }

        products = load_products()
        products.append(product)
        save_products(products)

        return redirect(url_for('admin'))

    products = load_products()
    categories = list({p.get('category', 'غير مصنف') for p in products})
    return render_template('admin.html', categories=categories)

@app.route('/products')
def products():
    products = load_products()
    categories = {}
    for p in products:
        cat = p.get('category', 'غير مصنف')
        categories.setdefault(cat, []).append(p)
    return render_template('products.html', categories=categories)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
