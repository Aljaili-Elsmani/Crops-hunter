from flask import Flask, render_template, request, redirect
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# الصفحة الرئيسية
@app.route('/')
def index():
    products = Product.query.all()

    products_by_category = {}
    for product in products:
        category = product.category or 'أخرى'
        if category not in products_by_category:
            products_by_category[category] = []
        products_by_category[category].append(product)

    return render_template('index.html', products_by_category=products_by_category)

# صفحة الإدارة لإضافة منتج
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form['unit']
        new_product = Product(name=name, category=category, price=price, unit=unit)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')

    return render_template('admin.html')

# صفحة "About Us"
@app.route('/about')
def about():
    return render_template('about.html')

# صفحة "Contact Us"
@app.route('/contact')
def contact():
    return render_template('contact.html')

# نقطة بدء التطبيق (فقط أثناء التطوير)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
