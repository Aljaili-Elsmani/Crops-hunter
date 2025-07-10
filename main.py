from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        products = Product.query.filter(Product.name.contains(search)).all()
    else:
        products = Product.query.all()

    # ترتيب المنتجات حسب الفئة
    products_by_category = {}
    for product in products:
        if product.category not in products_by_category:
            products_by_category[product.category] = []
        products_by_category[product.category].append(product)

    return render_template('index.html', products_by_category=products_by_category)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        unit = request.form['unit']
        origin = request.form['origin']
        quantity = request.form['quantity']
        notes = request.form['notes']

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
        return redirect('/admin')

    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
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
