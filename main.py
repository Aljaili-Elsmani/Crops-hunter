import os
from flask import Flask, render_template, request, redirect, url_for, flash
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
    # تصنيف المنتجات حسب الفئة في dict
    products_by_category = {}
    for p in products:
        products_by_category.setdefault(p.category, []).append(p)
    return render_template('index.html', products_by_category=products_by_category)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
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
    product = Product.query.get_or_404(product_id)
    # حذف الصورة من المجلد إذا موجودة
    if product.image_filename:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename))
        except:
            pass
    db.session.delete(product)
    db.session.commit()
    flash('تم حذف المنتج', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # إنشاء قاعدة البيانات لو لم تكن موجودة
    with app.app_context():
        db.create_all()
    app.run(debug=True)
