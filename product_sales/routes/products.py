from flask import jsonify, Blueprint, request

from product_sales import db
from product_sales.error_handlers import InvalidAPIUsage
from product_sales.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
def get_products():
    return jsonify(
        {'products': [product.to_dict() for product in Product.query.all()]}
    ), 200

@products_bp.route('', methods=['POST'])
def add_product():
    data = request.get_json()
    # Если есть недостающие ключи - выбрасываем собственное исключение
    if missing_keys:={'name', 'category_id'} - data.keys():
        raise InvalidAPIUsage(
            'В запросе отсутствуют обязательные поля: '
            f'{", ".join(missing_keys)}'
        )
    if Product.query.filter_by(name=data['name']).first() is not None:
        raise InvalidAPIUsage(
            f'Продукт с таким названием {data["name"]} уже есть в базе данных'
        )
    product = Product()
    product.from_dict(data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'product': product.to_dict()}), 201
