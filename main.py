from flask import Flask, render_template, request, redirect
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()

    # ترتيب المنتجات حسب الفئة
    products_by_category = {}
    for product in products:
        category = product.category or 'أخرى'
        if category not in products_by_category:
            products_by_category[category] = []
        products_by_category[category].append(product)

    return render_template('index.html', products_by_category=products_by_category)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        unit = request.form['unit']
        new_product = Product(name=name, price=price, category=category, unit=unit)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')
    
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/admin')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
