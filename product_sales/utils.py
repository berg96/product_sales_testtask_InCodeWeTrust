from datetime import datetime
from product_sales.error_handlers import InvalidAPIUsage


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        raise InvalidAPIUsage(
            f'Неверный формат даты: {date_str}. Ожидается формат DD-MM-YYYY'
        )
