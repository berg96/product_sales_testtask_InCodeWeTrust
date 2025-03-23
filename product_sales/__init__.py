from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

from . import cli_commands
from .models import Category, Product, Sale
from .routes import products_bp, sales_bp

app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)
