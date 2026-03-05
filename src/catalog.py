from sqlalchemy.orm import Session
from models import Region, Product, Price
from typing import List, Optional

class Catalog:
    """Работа с каталогом через SQLAlchemy сессию."""
    def __init__(self, session: Session):
        self.session = session

    def get_regions(self) -> List[str]:
        """Возвращает отсортированный список названий регионов."""
        regions = self.session.query(Region).order_by(Region.name).all()
        return [r.name for r in regions]

    def get_products_by_region(self, region_name: str) -> List[Product]:
        """Возвращает товары, имеющие цену для указанного региона."""
        region = self.session.query(Region).filter_by(name=region_name).first()
        if not region:
            return []
        # Загружаем товары вместе с ценами для этого региона
        products = (self.session.query(Product)
                    .join(Price)
                    .filter(Price.region_id == region.id)
                    .all())
        return products

    def get_cheapest_in_category(self, category_name: str, region_name: str) -> Optional[Product]:
        """Возвращает самый дешёвый товар в категории для региона."""
        region = self.session.query(Region).filter_by(name=region_name).first()
        if not region:
            return None
        product = (self.session.query(Product)
                   .join(Price)
                   .filter(Product.category.has(name=category_name))
                   .filter(Price.region_id == region.id)
                   .order_by(Price.price)
                   .first())
        return product

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).get(product_id)

    def get_price(self, product: Product, region_name: str) -> Optional[float]:
        """Получить цену товара для региона."""
        region = self.session.query(Region).filter_by(name=region_name).first()
        if not region:
            return None
        price_obj = self.session.query(Price).filter_by(product_id=product.id, region_id=region.id).first()
        return price_obj.price if price_obj else None