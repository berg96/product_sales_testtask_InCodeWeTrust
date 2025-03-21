from datetime import datetime

from . import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    products = db.relationship(
        'Product', backref='category', lazy='select', cascade='all, delete'
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name
        )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False
    )

    sales = db.relationship(
        'Sale', backref='product', lazy='dynamic', cascade='all, delete'
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            category=self.category.to_dict()
        )

    def from_dict(self, data):
        for field in ['name', 'category_id']:
            if field in data:
                setattr(self, field, data[field])


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(
        db.Date, default=datetime.utcnow().date(), nullable=False, index=True
    )
