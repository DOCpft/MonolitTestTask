class UI:
    @staticmethod
    def display_regions(regions: list) -> None:
        print("\nДоступные регионы:")
        for i, r in enumerate(regions, 1):
            print(f"{i}. {r}")

    @staticmethod
    def get_region_choice(regions: list) -> str:
        while True:
            try:
                choice = input("Выберите номер региона: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(regions):
                    return regions[idx]
                else:
                    print("Неверный номер. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")

    @staticmethod
    def display_products(products: list, region: str, catalog) -> None:
        """Показывает список товаров с ценами для региона."""
        print(f"\nТовары в регионе {region}:")
        for i, p in enumerate(products, 1):
            price = catalog.get_price(p, region)
            print(f"{i}. {p.name} (категория: {p.category.name}) - {price} руб.")

    @staticmethod
    def get_product_choice(products: list) -> object:
        while True:
            try:
                choice = input("Выберите номер товара: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(products):
                    return products[idx]
                else:
                    print("Неверный номер. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")

    @staticmethod
    def display_offer(product, price: float) -> None:
        print(f"\nПредложение: {product.name} - {price:.2f} руб.")

    @staticmethod
    def confirm(prompt: str) -> bool:
        while True:
            answer = input(f"{prompt} (y/n): ").strip().lower()
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print("Пожалуйста, введите 'y' или 'n'.")