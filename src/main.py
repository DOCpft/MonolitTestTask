from database import SessionLocal, init_db
from catalog import Catalog
from ui import UI
from order import OrderDto, save_order

def main():
    # Инициализация БД (создание таблиц и начальных данных при необходимости)
    init_db()

    # Создаём сессию
    session = SessionLocal()
    catalog = Catalog(session)

    try:
        # Выбор региона
        regions = catalog.get_regions()
        UI.display_regions(regions)
        region = UI.get_region_choice(regions)

        # Выбор товара
        products = catalog.get_products_by_region(region)
        if not products:
            print(f"Нет товаров для региона {region}.")
            return

        UI.display_products(products, region, catalog)
        selected_product = UI.get_product_choice(products)
        original_price = catalog.get_price(selected_product, region)
        UI.display_offer(selected_product, original_price)

        # Первичное подтверждение
        if UI.confirm("Оформляем заявку?"):
            order = OrderDto(region, selected_product, original_price)
            save_order(order)
            return

        # Отказ – ищем альтернативу
        print("\nИщем альтернативное предложение...")
        category_name = selected_product.category.name
        cheapest = catalog.get_cheapest_in_category(category_name, region)

        if not cheapest:
            print("Не удалось найти альтернативу в этой категории.")
            return

        if cheapest.id == selected_product.id:
            # Товар уже самый дешёвый – предлагаем скидку 5%
            discounted_price = original_price * 0.95
            UI.display_offer(selected_product, discounted_price)
            if UI.confirm("Оформляем заявку со скидкой 5%?"):
                order = OrderDto(region, selected_product, discounted_price)
                save_order(order)
            else:
                print("Заявка не оформлена.")
        else:
            # Предлагаем более дешёвый аналог
            alt_price = catalog.get_price(cheapest, region)
            UI.display_offer(cheapest, alt_price)
            if UI.confirm("Оформляем заявку на этот товар?"):
                order = OrderDto(region, cheapest, alt_price)
                save_order(order)
            else:
                print("Заявка не оформлена.")

    finally:
        session.close()

if __name__ == "__main__":
    main()