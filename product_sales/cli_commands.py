import csv
import random
from datetime import datetime, timedelta

import click

from . import app, db
from .models import Category, Product, Sale


@app.cli.command('load_test_data')
def load_test_data_command():
    """Функция загрузки тестовых данных в базу данных."""
    with open('categories.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            category = Category(**row)
            db.session.add(category)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено категорий: {counter}')
    with open('products.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            product = Product(**row)
            db.session.add(product)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено продуктов: {counter}')
    counter = 0
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=180)
    products = Product.query.all()
    for product in products:
        num_sales = random.randint(10, 50)
        for _ in range(num_sales):
            random_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            sale = Sale(
                product_id=product.id, quantity=random.randint(1, 10),
                date=random_date
            )
            db.session.add(sale)
            counter += 1
    db.session.commit()
    click.echo(f'Сгенерировано продаж: {counter}')
