from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# مسار رفع الصور
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# التحقق من امتداد الصورة
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# تسجيل فلتر تنسيق السعر
@app.template_filter('format_price')
def format_price(price_str):
    try:
        return "{:,}".format(int(str(price_str).replace(',', '').strip()))
    except ValueError:
        return price_str

# نموذج المنتج
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20))
    quantity = db.Column(db.String(50))
    origin = db.Column(db.String(100))
    production_date = db.Column(db.String(7))  # صيغة: YYYY-MM
    image_filename = db.Column(db.String(100))  # اسم ملف الصورة
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# الصفحة الرئيسية
@app.route('/')
def index():
    products = Product.query.all()
    products_by_category = {}
    for product in products:
        if product.category not in products_by_category:
            products_by_category[product.category] = []
        products_by_category[product.category].append(product)
    return render_template('index.html', products_by_category=products_by_category)

# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            flash("تم تسجيل الدخول بنجاح", 'success')
            return redirect(url_for('add_product'))
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة", 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("تم تسجيل الخروج", 'info')
    return redirect(url_for('index'))

# إضافة منتج
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form.get('unit', '')
        quantity = request.form.get('quantity', '')
        origin = request.form.get('origin', '')
        production_date = request.form.get('production_date', '')
        image = request.files.get('image')
        filename = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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
                production_date=production_date,
                image_filename=filename
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

# حذف منتج
@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not session.get('logged_in'):
        flash("يجب تسجيل الدخول", 'error')
        return redirect(url_for('login'))
    product = Product.query.get_or_404(product_id)
    if product.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    db.session.delete(product)
    db.session.commit()
    flash("تم حذف المنتج بنجاح", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
