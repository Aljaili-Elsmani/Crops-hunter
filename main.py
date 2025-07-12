from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)  # للحفاظ على تنسيق الفواصل
    unit = db.Column(db.String(20))
    quantity = db.Column(db.String(50))  # لتسمح بـ "100 كيلو"
    origin = db.Column(db.String(100))
    production_date = db.Column(db.String(50))  # بصيغة "07/2024"
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    products = Product.query.all()
    products_by_category = {}
    for product in products:
        products_by_category.setdefault(product.category, []).append(product)
    return render_template('index.html', products_by_category=products_by_category)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            flash("تم تسجيل الدخول بنجاح", 'success')
            return redirect(url_for('add_product'))
        flash("اسم المستخدم أو كلمة المرور غير صحيحة", 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("تم تسجيل الخروج", 'info')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form['unit']
        quantity = request.form['quantity']
        origin = request.form['origin']
        production_date = request.form['production_date']

        if not name or not category or not price:
            flash("يرجى ملء الحقول المطلوبة", 'error')
        else:
            new_product = Product(
                name=name,
                category=category,
                price=price,
                unit=unit,
                quantity=quantity,
                origin=origin,
                production_date=production_date
            )
            db.session.add(new_product)
            db.session.commit()
            flash("تمت إضافة المنتج بنجاح", 'success')
            return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
