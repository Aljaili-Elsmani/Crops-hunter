from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    name = db.Column(db.String(100))
    price = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        print("FORM DATA:", request.form)  # لمساعدتك على التحقق من صحة البيانات
        category = request.form.get('category')
        name = request.form.get('name')
        price = request.form.get('price')

        if category and name and price:
            new_product = Product(category=category, name=name, price=price)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "يرجى ملء جميع الحقول", 400

    return render_template('admin.html')

@app.route('/delete/<int:product_id>')
def delete(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
