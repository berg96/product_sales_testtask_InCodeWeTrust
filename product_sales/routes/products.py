from flask import Blueprint, jsonify, request
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
    if missing_keys := {'name', 'category_id'} - data.keys():
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


@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    if (
            'name' in data and
            Product.query.filter_by(name=data['name']).first() is not None
    ):
        # При неуникальном значении поля name возвращаем сообщение об ошибке
        raise InvalidAPIUsage(
            f'Продукт с таким названием {data["name"]} уже есть в базе данных'
        )
    product = Product.query.get(id)
    if product is None:
        raise InvalidAPIUsage('Продукт с указанным id не найден', 404)
    # Если поле для изменения не указано, оставляем исходное значение
    product.name = data.get('name', product.name)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({'product': product.to_dict()}), 200


@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        raise InvalidAPIUsage('Продукт с указанным id не найден', 404)
    db.session.delete(product)
    db.session.commit()
    return '', 204
