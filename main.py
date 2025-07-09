from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# نموذج قاعدة البيانات
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    seller = db.Column(db.String(100), nullable=True)

# الصفحة الرئيسية تعرض كل المنتجات
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# صفحة إضافة منتج (الإدارة)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        seller = request.form['seller']

        new_product = Product(name=name, category=category, price=price, seller=seller)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('admin.html')

# حذف منتج
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
