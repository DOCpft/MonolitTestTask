import json
import os
from datetime import datetime
from models import Product

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS_DIR = os.path.join(BASE_DIR, 'orders')

class OrderDto:
    """Модель заявки."""
    def __init__(self, region: str, product: Product, price: float):
        self.region = region
        self.product = product
        self.price = price
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        return {
            "region": self.region,
            "product_id": self.product.id,
            "product_name": self.product.name,
            "category": self.product.category.name,
            "price": round(self.price, 2),
            "timestamp": self.timestamp.isoformat()
        }

def save_order(order: OrderDto, filename: str = None) -> None:
    if filename is None:
        filename = f"order_{order.timestamp.strftime('%Y%m%d_%H%M%S')}.json"

    filepath = os.path.join(ORDERS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(order.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"Заявка сохранена в файл {filepath}")