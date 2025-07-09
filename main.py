from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# نموذج المنتج
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.String(50))
    unit = db.Column(db.String(50))
    seller = db.Column(db.String(100))

# إنشاء قاعدة البيانات إذا لم تكن موجودة
with app.app_context():
    db.create_all()

# 🏠 الصفحة الرئيسية: عرض المنتجات
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# ➕ صفحة إضافة منتج
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form['unit']
        seller = request.form['seller']

        new_product = Product(name=name, category=category, price=price, unit=unit, seller=seller)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('admin.html')

# 🗑️ حذف منتج
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

# 🚀 تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
