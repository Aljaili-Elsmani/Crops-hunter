from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# موديل المنتج
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Product {self.name}>'

# إنشاء الجداول (قاعدة البيانات) عند تشغيل التطبيق
with app.app_context():
    db.create_all()

# الصفحة الرئيسية - عرض المنتجات
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# صفحة الإدارة - إضافة وعرض المنتجات
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # قراءة بيانات المنتج من الفورم
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        unit = request.form['unit']
        origin = request.form.get('origin', '')
        quantity = request.form.get('quantity', '')
        notes = request.form.get('notes', '')

        # إنشاء وإضافة المنتج لقاعدة البيانات
        new_product = Product(
            name=name,
            category=category,
            price=price,
            unit=unit,
            origin=origin,
            quantity=quantity,
            notes=notes
        )
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    # عرض كل المنتجات في صفحة الإدارة
    products = Product.query.all()
    return render_template('admin.html', products=products)

# صفحة تفاصيل المنتج
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
