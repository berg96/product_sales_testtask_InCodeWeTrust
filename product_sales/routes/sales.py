from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import func

from product_sales import db
from product_sales.models import Sale
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
