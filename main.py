from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# نموذج المنتج
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Product {self.name}>'

# الصفحة الرئيسية - عرض المنتجات حسب الفئة
@app.route('/')
def index():
    products = Product.query.all()
    products_by_category = {}
    for product in products:
        if product.category not in products_by_category:
            products_by_category[product.category] = []
        products_by_category[product.category].append(product)
    return render_template('index.html', products_by_category=products_by_category)

# إدارة المنتجات - إضافة وعرض
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        unit = request.form['unit']
        origin = request.form.get('origin')
        quantity = request.form.get('quantity')
        notes = request.form.get('notes')

        new_product = Product(
            name=name, category=category, price=price, unit=unit,
            origin=origin, quantity=quantity, notes=notes
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin'))

    products = Product.query.all()
    return render_template('admin.html', products=products)

# حذف منتج
@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin'))

# عرض تفاصيل المنتج
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

# تشغيل التطبيق
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
