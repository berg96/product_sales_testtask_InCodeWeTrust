from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import func

from product_sales import db
from product_sales.models import Sale, Product
from product_sales.error_handlers import InvalidAPIUsage


sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')


@sales_bp.route('/total', methods=['GET'])
def get_total_sales():
    # Запрос не должен быть пустой
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage(
            'В запросе должны быть обязательные параметры: '
            'start_date и end_date'
        )
    # Если есть недостающие ключи - выбрасываем собственное исключение
    if missing_keys := {'start_date', 'end_date'} - data.keys():
        raise InvalidAPIUsage(
            'В запросе отсутствуют обязательные поля: '
            f'{", ".join(missing_keys)}'
        )
    return jsonify({'total': db.session.query(func.sum(Sale.quantity)).filter(
        Sale.date.between(
            datetime.strptime(data['start_date'], '%d.%m.%Y').date(),
            datetime.strptime(data['end_date'], '%d.%m.%Y').date()
        )
    ).scalar()})

@sales_bp.route('/top-products', methods=['GET'])
def get_top_products():
    # Запрос не должен быть пустой
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage(
            'В запросе должны быть обязательные параметры: '
            'start_date, end_date и limit'
        )
    # Если есть недостающие ключи - выбрасываем собственное исключение
    if missing_keys := {'start_date', 'end_date', 'limit'} - data.keys():
        raise InvalidAPIUsage(
            'В запросе отсутствуют обязательные поля: '
            f'{", ".join(missing_keys)}'
        )
    return jsonify(
        {'top_products': [
            # Выводим сериализованный продукт и сумму продаж этого продукта
            {
                'product': product.to_dict(),
                'total_sales': total
            # Извлекаем из БД Продукт и Сумму продаж,
            # сгруппированную по Продукту, отфильтрованную по параметрам
            # и отсортированную по убыванию
            } for product, total in db.session.query(
                Product, func.sum(Sale.quantity).label('total')
            )
            .join(Sale, Product.id == Sale.product_id)
            .filter(Sale.date.between(
                datetime.strptime(data['start_date'], '%d.%m.%Y').date(),
                datetime.strptime(data['end_date'], '%d.%m.%Y').date()
            ))
            .group_by(Product)
            .order_by(func.sum(Sale.quantity).desc())
            .limit(data['limit'])
            .all()
        ]}
    )
