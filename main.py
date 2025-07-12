from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Product
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

# فلتر لتنسيق السعر
@app.template_filter('format_price')
def format_price_filter(price):
    try:
        return "{:,}".format(int(str(price).replace(",", "")))
    except:
        return price

@app.route('/')
def index():
    products = Product.query.all()
    products_by_category = {}
    for product in products:
        if product.category not in products_by_category:
            products_by_category[product.category] = []
        products_by_category[product.category].append(product)
    return render_template('index.html', products_by_category=products_by_category)

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
        image_filename = None

        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

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
                image_filename=image_filename
            )
            db.session.add(new_product)
            db.session.commit()
            flash("تمت إضافة المنتج بنجاح", 'success')
            return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("تم حذف المنتج", 'info')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
