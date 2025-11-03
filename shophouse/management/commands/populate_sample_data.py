from django.core.management.base import BaseCommand
from django.utils import timezone
from shophouse.models import Product, Categories, Order, Profile, Customer
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create categories if they don't exist
        categories = [
            "Electronics",
            "Fashion",
            "Home & Living",
            "Health & Beauty",
            "Sports & Outdoor"
        ]
        
        category_objects = {}
        for cat_name in categories:
            category, created = Categories.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = category
            if created:
                self.stdout.write(f"Created category: {cat_name}")

        # Sample products with realistic data
        products_data = [
            {
                "name": "Smart LED TV",
                "description": "43-inch Smart LED TV with HD resolution",
                "price": 899000,
                "category": "Electronics",
                "is_sale": True,
                "sale_price": 799000
            },
            {
                "name": "Smartphone X12",
                "description": "Latest smartphone with 128GB storage",
                "price": 699000,
                "category": "Electronics",
                "is_sale": False,
                "sale_price": 699000
            },
            {
                "name": "Designer Dress",
                "description": "Elegant evening dress",
                "price": 120000,
                "category": "Fashion",
                "is_sale": True,
                "sale_price": 95000
            },
            {
                "name": "Running Shoes",
                "description": "Professional running shoes",
                "price": 150000,
                "category": "Sports & Outdoor",
                "is_sale": False,
                "sale_price": 150000
            },
            {
                "name": "Coffee Maker",
                "description": "Automatic coffee maker with timer",
                "price": 85000,
                "category": "Home & Living",
                "is_sale": True,
                "sale_price": 75000
            },
            {
                "name": "Skin Care Set",
                "description": "Complete skin care package",
                "price": 65000,
                "category": "Health & Beauty",
                "is_sale": False,
                "sale_price": 65000
            },
            {
                "name": "Gaming Console",
                "description": "Latest gaming console with controllers",
                "price": 1200000,
                "category": "Electronics",
                "is_sale": True,
                "sale_price": 1100000
            },
            {
                "name": "Yoga Mat",
                "description": "Premium non-slip yoga mat",
                "price": 45000,
                "category": "Sports & Outdoor",
                "is_sale": False,
                "sale_price": 45000
            },
            {
                "name": "Kitchen Blender",
                "description": "High-power kitchen blender",
                "price": 135000,
                "category": "Home & Living",
                "is_sale": True,
                "sale_price": 115000
            },
            {
                "name": "Hair Dryer Pro",
                "description": "Professional hair dryer with attachments",
                "price": 78000,
                "category": "Health & Beauty",
                "is_sale": False,
                "sale_price": 78000
            }
        ]

        # Create products
        product_objects = []
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "Category": category_objects[product_data["category"]],
                    "is_sale": product_data["is_sale"],
                    "sale_price": product_data["sale_price"]
                }
            )
            product_objects.append(product)
            if created:
                self.stdout.write(f"Created product: {product.name}")

        # Create sample users if they don't exist
        users_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "user_name": "johndoe",
                "email": "john@example.com",
                "password": "password123"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "user_name": "janesmith",
                "email": "jane@example.com",
                "password": "password123"
            },
            {
                "first_name": "Bob",
                "last_name": "Johnson",
                "user_name": "bjohnson",
                "email": "bob@example.com",
                "password": "password123"
            }
        ]

        customer_objects = []
        for user_data in users_data:
            profile, created = Profile.objects.get_or_create(
                user_name=user_data["user_name"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
            )
            customer, created = Customer.objects.get_or_create(UserName=profile)
            customer_objects.append(customer)
            if created:
                self.stdout.write(f"Created customer: {profile.user_name}")

        # Generate random orders over the past 6 months
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)
        
        # Generate 100 random orders
        for _ in range(100):
            order_date = start_date + timedelta(
                days=random.randint(0, 180)
            )
            
            product = random.choice(product_objects)
            customer = random.choice(customer_objects)
            quantity = random.randint(1, 5)
            status = random.choice([True, False])  # Randomly set as delivered or pending
            
            order = Order.objects.create(
                product=product,
                customer=customer,
                quantity=quantity,
                orderDate=order_date,
                address="Sample Address",
                phone="0123456789",
                status=status
            )
            self.stdout.write(f"Created order: {order.id} for {product.name}")

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))