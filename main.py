import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret_key_here'  # غيرها لمفتاح آمن
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# مجلد حفظ الصور
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# السماح فقط بامتدادات معينة
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# نموذج المنتج مع حقل اسم الصورة
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    production_date = db.Column(db.String(20), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# فلتر لتنسيق السعر مع فواصل الآلاف
@app.template_filter('format_price')
def format_price_filter(price):
    try:
        return "{:,}".format(int(price))
    except:
        return price

@app.route('/')
def index():
    products = Product.query.all()
    products_by_category = {}
    for p in products:
        products_by_category.setdefault(p.category, []).append(p)
    return render_template('index.html', products_by_category=products_by_category)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not session.get('logged_in'):
        flash('يجب تسجيل الدخول لإضافة منتج', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        origin = request.form.get('origin')
        production_date = request.form.get('production_date')

        image = request.files.get('image')
        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            if image and image.filename != '':
                flash('نوع الملف غير مدعوم', 'error')
                return redirect(request.url)

        if not name or not category or not price:
            flash('الرجاء تعبئة الحقول المطلوبة', 'error')
            return redirect(request.url)

        new_product = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            origin=origin,
            production_date=production_date,
            image_filename=filename
        )
        db.session.add(new_product)
        db.session.commit()
        flash('تم إضافة المنتج بنجاح', 'success')
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not session.get('logged_in'):
        flash('غير مصرح لك بحذف المنتج', 'error')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(product_id)
    if product.image_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename))
        except:
            pass
    db.session.delete(product)
    db.session.commit()
    flash('تم حذف المنتج', 'success')
    return redirect(url_for('index'))

# صفحة تسجيل الدخول للمشرف (مثال بسيط)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # غيرها حسب بياناتك الحقيقية
        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('index'))
        else:
            flash('بيانات الدخول غير صحيحة', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('تم تسجيل الخروج', 'info')
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # الاستماع على كل الواجهات حتى Render يقدر يشغل التطبيق
    app.run(host='0.0.0.0', debug=True)
