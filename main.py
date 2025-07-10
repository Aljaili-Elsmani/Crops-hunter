from flask import Flask, render_template, request, redirect, url_for
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
    products = Product.query.order_by(Product.category).all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        unit = request.form['unit']
        origin = request.form.get('origin')
        quantity = request.form.get('quantity')
        notes = request.form.get('notes')

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

    products = Product.query.all()
    return render_template('admin.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
