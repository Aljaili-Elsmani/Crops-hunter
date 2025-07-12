from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20))
    quantity = db.Column(db.String(50))
    origin = db.Column(db.String(100))
    production_date = db.Column(db.String(7))  # صيغة: YYYY-MM
    image_filename = db.Column(db.String(200))  # لتخزين اسم الصورة
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
