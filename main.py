from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # أنشأنا SQLAlchemy بدون ربط مباشر

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from models import Product

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        search = request.args.get('search', '')
        if search:
            products = Product.query.filter(Product.name.contains(search)).all()
        else:
            products = Product.query.all()

        products_by_category = {}
        for product in products:
            category = product.category
            if category not in products_by_category:
                products_by_category[category] = []
            products_by_category[category].append(product)

        return render_template('index.html', products_by_category=products_by_category)

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if request.method == 'POST':
            name = request.form['name']
            category = request.form['category']
            price = request.form['price']
            unit = request.form['unit']
            origin = request.form['origin']
            availability = request.form['availability']
            notes = request.form['notes']

            product = Product(
                name=name,
                category=category,
                price=price,
                unit=unit,
                origin=origin,
                availability=availability,
                notes=notes
            )
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('admin'))

        products = Product.query.all()
        return render_template('admin.html', products=products)

    @app.route('/delete/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
        return redirect(url_for('admin'))

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
