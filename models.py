from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
