"""
Management-команда для наполнения базы тестовыми данными.

КУДА ПОЛОЖИТЬ ФАЙЛ:
    avito_app/management/commands/seed_data.py

Если папок management/commands ещё нет — создай их вручную:
    avito_app/
        management/
            __init__.py            (пустой файл)
            commands/
                __init__.py        (пустой файл)
                seed_data.py       (этот файл)

КАК ЗАПУСТИТЬ:
    python manage.py seed_data

Команда создаёт: пользователей, категории, подкатегории, товары,
изображения товаров и отзывы. Для полей category_name / subcategory_name /
product_name заполняются обе локали (en и ru) — это работает благодаря
modeltranslation, который добавляет к каждому переводимому полю
суффиксы _en и _ru автоматически (category_name_en, category_name_ru и т.д.).
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from avito_app.models import (
    UserProfile,
    Category,
    SubCategory,
    Product,
    ProductImage,
    Review,
)


class Command(BaseCommand):
    help = "Наполняет базу тестовыми данными для всех моделей avito_app (с переводами en/ru)."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Начинаю наполнение базы данными...")

        users = self.create_users()
        categories = self.create_categories()
        subcategories = self.create_subcategories(categories)
        products = self.create_products(subcategories)
        self.create_product_images(products)
        self.create_reviews(users, products)

        self.stdout.write(self.style.SUCCESS("Готово! Тестовые данные успешно добавлены."))

    # ------------------------------------------------------------------
    # UserProfile
    # ------------------------------------------------------------------
    def create_users(self):
        self.stdout.write("Создаю пользователей...")

        users_data = [
            {
                "username": "gold_user",
                "email": "gold_user@example.com",
                "age": 28,
                "phone_number": "+996700111222",
                "status": "gold",
            },
            {
                "username": "silver_user",
                "email": "silver_user@example.com",
                "age": 34,
                "phone_number": "+996700333444",
                "status": "silver",
            },
            {
                "username": "bronze_user",
                "email": "bronze_user@example.com",
                "age": 22,
                "phone_number": "+996700555666",
                "status": "bronze",
            },
            {
                "username": "simple_user",
                "email": "simple_user@example.com",
                "age": 19,
                "phone_number": "+996700777888",
                "status": "simple",
            },
        ]

        users = []
        for data in users_data:
            user, created = UserProfile.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "age": data["age"],
                    "phone_number": data["phone_number"],
                    "status": data["status"],
                },
            )
            if created:
                user.set_password("testpass123")
                user.save()
            users.append(user)

        return users

    # ------------------------------------------------------------------
    # Category (переводимое поле: category_name -> category_name_en / _ru)
    # ------------------------------------------------------------------
    def create_categories(self):
        self.stdout.write("Создаю категории...")

        categories_data = [
            {"en": "Electronics", "ru": "Электроника"},
            {"en": "Clothing", "ru": "Одежда"},
            {"en": "Home & Garden", "ru": "Дом и сад"},
        ]

        categories = []
        for data in categories_data:
            category, _ = Category.objects.get_or_create(
                category_name_en=data["en"],
                defaults={
                    "category_name_ru": data["ru"],
                    "category_image": "category_image/placeholder.jpg",
                },
            )
            # На случай если запись уже существовала без перевода ru
            if not category.category_name_ru:
                category.category_name_ru = data["ru"]
                category.save()
            categories.append(category)

        return categories

    # ------------------------------------------------------------------
    # SubCategory (переводимое поле: subcategory_name)
    # ------------------------------------------------------------------
    def create_subcategories(self, categories):
        self.stdout.write("Создаю подкатегории...")

        electronics, clothing, home_garden = categories

        subcategories_data = [
            {"category": electronics, "en": "Smartphones", "ru": "Смартфоны"},
            {"category": electronics, "en": "Laptops", "ru": "Ноутбуки"},
            {"category": clothing, "en": "Men's Clothing", "ru": "Мужская одежда"},
            {"category": clothing, "en": "Women's Clothing", "ru": "Женская одежда"},
            {"category": home_garden, "en": "Furniture", "ru": "Мебель"},
        ]

        subcategories = []
        for data in subcategories_data:
            subcategory, _ = SubCategory.objects.get_or_create(
                category=data["category"],
                subcategory_name_en=data["en"],
                defaults={
                    "subcategory_name_ru": data["ru"],
                    "subcategory_image": "subcategory_image/placeholder.jpg",
                },
            )
            if not subcategory.subcategory_name_ru:
                subcategory.subcategory_name_ru =data["ru"]
                subcategory.save()
            subcategories.append(subcategory)

        return subcategories

    # ------------------------------------------------------------------
    # Product (переводимое поле: product_name)
    # ------------------------------------------------------------------
    def create_products(self, subcategories):
        self.stdout.write("Создаю товары...")

        smartphones, laptops, mens, womens, furniture = subcategories

        products_data = [
            {
                "subcategory": smartphones,
                "en": "iPhone 15 Pro",
                "ru": "iPhone 15 Pro",
                "price": "999.99",
                "description_en": "Latest Apple smartphone with A17 chip.",
                "article_image": 1001,
            },
            {
                "subcategory": smartphones,
                "en": "Samsung Galaxy S24",
                "ru": "Samsung Galaxy S24",
                "price": "849.99",
                "description_en": "Flagship Samsung smartphone.",
                "article_image": 1002,
            },
            {
                "subcategory": laptops,
                "en": "MacBook Air M3",
                "ru": "MacBook Air M3",
                "price": "1299.00",
                "description_en": "Lightweight laptop with M3 chip.",
                "article_image": 1003,
            },
            {
                "subcategory": mens,
                "en": "Denim Jacket",
                "ru": "Джинсовая куртка",
                "price": "59.90",
                "description_en": "Classic blue denim jacket.",
                "article_image": 1004,
            },
            {
                "subcategory": womens,
                "en": "Summer Dress",
                "ru": "Летнее платье",
                "price": "39.50",
                "description_en": "Light floral summer dress.",
                "article_image": 1005,
            },
            {
                "subcategory": furniture,
                "en": "Office Chair",
                "ru": "Офисное кресло",
                "price": "149.00",
                "description_en": "Ergonomic office chair with lumbar support.",
                "article_image": 1006,
            },
        ]

        products = []
        for data in products_data:
            product, _ = Product.objects.get_or_create(
                article_image=data["article_image"],
                defaults={
                    "subcategory": data["subcategory"],
                    "product_name_en": data["en"],
                    "product_name_ru": data["ru"],
                    "price": data["price"],
                    "description": data["description_en"],
                    "product_type": True,
                },
            )
            if not product.product_name_ru:
                product.product_name_ru = data["ru"]
                product.save()
            products.append(product)

        return products

    # ------------------------------------------------------------------
    # ProductImage
    # ------------------------------------------------------------------
    def create_product_images(self, products):
        self.stdout.write("Создаю изображения товаров...")

        for product in products:
            for i in range(1, 3):  # по 2 изображения на товар
                ProductImage.objects.get_or_create(
                    product=product,
                    product_image=f"product_image/{product.pk}_{i}.jpg",
                )

    # ------------------------------------------------------------------
    # Review
    # ------------------------------------------------------------------
    def create_reviews(self, users, products):
        self.stdout.write("Создаю отзывы...")

        review_texts = [
            "Отличный товар, всё понравилось!",
            "Хорошее качество за свою цену.",
            "Есть небольшие недостатки, но в целом доволен.",
            "Быстрая доставка, товар как на фото.",
            "Не совсем то, что ожидал, но пользоваться можно.",
        ]

        review_index = 0
        for product in products:
            # каждому товару — 2 отзыва от разных пользователей
            for user in users[:2]:
                stars = str((review_index % 5) + 1)
                Review.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={
                        "stars": stars,
                        "comment": review_texts[review_index % len(review_texts)],
                    },
                )
                review_index += 1