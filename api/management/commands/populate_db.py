from django.core.management.base import BaseCommand
from api.models import User, Product, Order, OrderItem
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заповнює базу даних тестовими даними'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очищення існуючих даних...')

        # Очищення даних
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Створення користувача...')

        # Створення користувача
        user = User.objects.create_user(
            username='skhmelyuk',
            email='skhmelyuk@example.com',
            password='qwerty_1985'
        )

        self.stdout.write('Створення продуктів...')

        # Створення продуктів
        products_data = [
            {
                'name': 'Ноутбук Dell XPS 15',
                'description': 'Потужний ноутбук для роботи та розваг',
                'price': Decimal('45000.00'),
                'stock': 10
            },
            {
                'name': 'iPhone 15 Pro',
                'description': 'Новітній смартфон від Apple',
                'price': Decimal('35000.00'),
                'stock': 15
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Флагманський смартфон Samsung',
                'price': Decimal('30000.00'),
                'stock': 20
            },
            {
                'name': 'AirPods Pro',
                'description': 'Бездротові навушники з шумозаглушенням',
                'price': Decimal('8000.00'),
                'stock': 50
            },
            {
                'name': 'iPad Air',
                'description': 'Універсальний планшет для будь-яких задач',
                'price': Decimal('20000.00'),
                'stock': 25
            },
            {
                'name': 'MacBook Pro 14"',
                'description': 'Професійний ноутбук з чіпом M3',
                'price': Decimal('65000.00'),
                'stock': 8
            },
            {
                'name': 'Apple Watch Series 9',
                'description': 'Розумний годинник з функціями здоров\'я',
                'price': Decimal('12000.00'),
                'stock': 30
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Преміум навушники з шумозаглушенням',
                'price': Decimal('11000.00'),
                'stock': 15
            },
        ]

        products = []
        for product_data in products_data:
            product = Product.objects.create(**product_data)
            products.append(product)
            self.stdout.write(f'  ✓ Створено: {product.name}')

        self.stdout.write('Створення замовлень...')

        # Створення замовлень
        for i in range(3):
            order = Order.objects.create(
                user=user,
                status=random.choice([
                    Order.StatusChoices.PENDING,
                    Order.StatusChoices.COMPLETED
                ])
            )

            # Додавання випадкових продуктів до замовлення
            selected_products = random.sample(products, k=random.randint(2, 4))

            for product in selected_products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 3)
                )

            self.stdout.write(f'  ✓ Створено замовлення: {order.order_id}')

        self.stdout.write(self.style.SUCCESS('\n✅ База даних успішно заповнена!'))
        self.stdout.write(f'Користувачів: {User.objects.count()}')
        self.stdout.write(f'Продуктів: {Product.objects.count()}')
        self.stdout.write(f'Замовлень: {Order.objects.count()}')
        self.stdout.write(f'Елементів замовлень: {OrderItem.objects.count()}')