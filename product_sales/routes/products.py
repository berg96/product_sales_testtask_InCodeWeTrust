from flask import jsonify, Blueprint

from product_sales.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
def get_products():
    return jsonify(
        {'products': [product.to_dict() for product in Product.query.all()]}
    ), 200
