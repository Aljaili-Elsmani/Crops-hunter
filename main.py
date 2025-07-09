from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تعريف جدول المنتجات
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    seller = db.Column(db.String(100), nullable=False)

# إنشاء قاعدة البيانات عند التشغيل لأول مرة
with app.app_context():
    db.create_all()

# الصفحة الرئيسية – عرض كل المنتجات
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# صفحة الإضافة
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        seller = request.form['seller']

        new_product = Product(name=name, price=price, category=category, seller=seller)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('index'))  # تحويل مباشر للصفحة الرئيسية بعد الإضافة

    return render_template('admin.html')

# حذف منتج
@app.route('/delete/<int:product_id>')
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
