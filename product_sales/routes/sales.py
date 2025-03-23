from flask import Blueprint, request, jsonify
from sqlalchemy import func

from product_sales import db
from product_sales.cache import get_from_cache, set_to_cache
from product_sales.models import Sale, Product
from product_sales.error_handlers import InvalidAPIUsage
from product_sales.utils import validate_date

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')


@sales_bp.route('/total', methods=['GET'])
def get_total_sales():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # Если есть недостающие параметры - выбрасываем собственное исключение
    if not start_date or not end_date:
        raise InvalidAPIUsage(
            'В запросе должны быть обязательные параметры: '
            'start_date и end_date'
        )
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    if end_date < start_date:
        raise InvalidAPIUsage(
            'Параметр end_date должен быть больше start_date'
        )
    cache_key = f'get_total_sales_{start_date}_{end_date}'
    if cached_result := get_from_cache(cache_key):
        return jsonify({'cached': True, 'total': cached_result})
    total_sales = db.session.query(func.sum(Sale.quantity)).filter(
        Sale.date.between(start_date, end_date)
    ).scalar()
    set_to_cache(cache_key, total_sales)
    return jsonify({'cached': False, 'total': total_sales})

@sales_bp.route('/top-products', methods=['GET'])
def get_top_products():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int)
    # Если есть недостающие параметры - выбрасываем собственное исключение
    if not start_date or not end_date or not limit:
        raise InvalidAPIUsage(
            'В запросе должны быть обязательные параметры: '
            'start_date, end_date и limit'
        )
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    if end_date < start_date:
        raise InvalidAPIUsage(
            'Параметр end_date должен быть больше start_date'
        )
    cache_key = f'get_top_products_{start_date}_{end_date}_{limit}'
    if cached_result := get_from_cache(cache_key):
        return jsonify({'cached': True, 'top_products': cached_result})
    top_products = [
        # Задаем список словарей из
        # сериализованного продукта и сумму продаж этого продукта
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
        .filter(Sale.date.between(start_date, end_date))
        .group_by(Product)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(limit)
        .all()
    ]
    set_to_cache(cache_key, top_products)
    return jsonify({'cached': False, 'top_products': top_products})
