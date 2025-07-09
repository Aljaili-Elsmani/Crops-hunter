from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# الصفحة الرئيسية
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# إدارة المنتجات (إضافة / حذف)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        price = request.form['price']
        new_product = Product(category=category, name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin'))

    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin'))

# صفحة "للتواصل معنا"
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحة "من نحن"
@app.route('/about')
def about():
    return render_template('about.html')

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
