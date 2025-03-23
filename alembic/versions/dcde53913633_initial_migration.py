"""Initial migration

Revision ID: dcde53913633
Revises:
Create Date: 2025-03-21 00:24:11.645511

"""
import csv
import random
from datetime import datetime, timedelta
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dcde53913633'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'],),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'sale',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sale_date'), 'sale', ['date'], unique=False)
    # ### end Alembic commands ###
    with open('categories.csv', encoding='utf-8') as file:
        categories = list(csv.DictReader(file))
    op.bulk_insert(
        sa.table(
            'category',
            sa.Column('name', sa.String)
        ),
        categories
    )
    with open('products.csv', encoding='utf-8') as f:
        products = list(csv.DictReader(f))
    op.bulk_insert(
        sa.table(
            'product',
            sa.Column('name', sa.String),
            sa.Column('category_id', sa.Integer)
        ),
        products
    )
    sales = []
    start_date = datetime.utcnow().date() - timedelta(days=180)
    for product_id in range(1, len(products) + 1):
        number_sales = random.randint(10, 50)
        for _ in range(number_sales):
            sales.append({
                'product_id': product_id,
                'quantity': random.randint(1, 10),
                'date': start_date + timedelta(days=random.randint(0, 180))
            })
    op.bulk_insert(
        sa.table(
            'sale',
            sa.Column('product_id', sa.Integer),
            sa.Column('quantity', sa.Integer),
            sa.Column('date', sa.Date)
        ),
        sales
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sale_date'), table_name='sale')
    op.drop_table('sale')
    op.drop_table('product')
    op.drop_table('category')
    # ### end Alembic commands ###
