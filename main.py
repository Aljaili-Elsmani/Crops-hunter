from flask import Flask, render_template, request, redirect
from models import db, Product
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# الصفحة الرئيسية
@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
    else:
        products = Product.query.all()
    
    products_by_category = {}
    for product in products:
        category = product.category or 'أخرى'
        if category not in products_by_category:
            products_by_category[category] = []
        products_by_category[category].append(product)
    return render_template('index.html', products_by_category=products_by_category)

# صفحة إدارة المنتجات
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form['unit']
        new_product = Product(name=name, category=category, price=price, unit=unit)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')
    products = Product.query.all()
    return render_template('admin.html', products=products)

# حذف منتج
@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect('/admin')

# صفحة About
@app.route('/about')
def about():
    return render_template('about.html')

# صفحة Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# تشغيل التطبيق
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
