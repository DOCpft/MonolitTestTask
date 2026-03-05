import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'materials.db')

Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Создаёт таблицы и заполняет начальными данными, если БД пуста."""
    Base.metadata.create_all(engine)
    # Проверка, есть ли уже данные
    from models import Region, Category, Product, Price
    session = SessionLocal()
    if session.query(Region).count() == 0:
        # Регионы
        regions = [
            Region(name='Москва'),
            Region(name='СПб'),
            Region(name='Казань')
        ]
        session.add_all(regions)
        session.flush()  # чтобы получить id

        # Категории
        categories = [
            Category(name='Кирпич'),
            Category(name='Бетон'),
            Category(name='Пиломатериалы'),
            Category(name='Кровля'),
            Category(name='Утеплитель')
        ]
        session.add_all(categories)
        session.flush()

        # Товары (не менее 10)
        products_data = [
            ('Кирпич красный', 'Кирпич'),
            ('Кирпич силикатный', 'Кирпич'),
            ('Бетон М300', 'Бетон'),
            ('Бетон М400', 'Бетон'),
            ('Доска обрезная', 'Пиломатериалы'),
            ('Брус 100x100', 'Пиломатериалы'),
            ('Металлочерепица', 'Кровля'),
            ('Ондулин', 'Кровля'),
            ('Минеральная вата', 'Утеплитель'),
            ('Пенопласт', 'Утеплитель'),
        ]

        # Цены для каждого товара по регионам
        prices_data = {
            'Кирпич красный': {'Москва': 12, 'СПб': 11, 'Казань': 10},
            'Кирпич силикатный': {'Москва': 10, 'СПб': 9, 'Казань': 8},
            'Бетон М300': {'Москва': 3500, 'СПб': 3400, 'Казань': 3300},
            'Бетон М400': {'Москва': 3800, 'СПб': 3700, 'Казань': 3600},
            'Доска обрезная': {'Москва': 800, 'СПб': 750, 'Казань': 700},
            'Брус 100x100': {'Москва': 1200, 'СПб': 1150, 'Казань': 1100},
            'Металлочерепица': {'Москва': 500, 'СПб': 480, 'Казань': 460},
            'Ондулин': {'Москва': 300, 'СПб': 290, 'Казань': 280},
            'Минеральная вата': {'Москва': 1500, 'СПб': 1450, 'Казань': 1400},
            'Пенопласт': {'Москва': 1200, 'СПб': 1150, 'Казань': 1100},
        }

        # Создаём товары и цены
        for prod_name, cat_name in products_data:
            category = session.query(Category).filter_by(name=cat_name).first()
            product = Product(name=prod_name, category=category)
            session.add(product)
            session.flush()

            # Добавляем цены
            region_prices = prices_data[prod_name]
            for reg_name, price_val in region_prices.items():
                region = session.query(Region).filter_by(name=reg_name).first()
                price = Price(product=product, region=region, price=price_val)
                session.add(price)

        session.commit()
    session.close()