from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from shophouse.models import Product, Categories, Order, Profile, Customer
from datetime import datetime, timedelta
import random
import os
from django.conf import settings
import shutil

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
                "sale_price": 799000,
                "image": "freepic.jpg"
            },
            {
                "name": "Smartphone X12",
                "description": "Latest smartphone with 128GB storage",
                "price": 699000,
                "category": "Electronics",
                "is_sale": False,
                "sale_price": 699000,
                "image": "phone.jpg"
            },
            {
                "name": "Designer Shirt",
                "description": "Elegant designer shirt",
                "price": 120000,
                "category": "Fashion",
                "is_sale": True,
                "sale_price": 95000,
                "image": "shirts.jpg"
            },
            {
                "name": "Running Shoes",
                "description": "Professional running shoes",
                "price": 150000,
                "category": "Sports & Outdoor",
                "is_sale": False,
                "sale_price": 150000,
                "image": "shoe.jpg"
            },
            {
                "name": "Luxury Perfume",
                "description": "Premium luxury perfume",
                "price": 85000,
                "category": "Health & Beauty",
                "is_sale": True,
                "sale_price": 75000,
                "image": "perfume.jpg"
            },
            {
                "name": "Gucci Bag",
                "description": "Authentic Gucci designer bag",
                "price": 650000,
                "category": "Fashion",
                "is_sale": False,
                "sale_price": 650000,
                "image": "gucci.jpg"
            },
            {
                "name": "Sport Shoes Pro",
                "description": "Professional sports footwear",
                "price": 200000,
                "category": "Sports & Outdoor",
                "is_sale": True,
                "sale_price": 180000,
                "image": "shoe1.jpg"
            },
            {
                "name": "Classic Shirt",
                "description": "Premium cotton classic shirt",
                "price": 45000,
                "category": "Fashion",
                "is_sale": False,
                "sale_price": 45000,
                "image": "shirt2.jpg"
            },
            {
                "name": "Smart Device",
                "description": "Latest smart home device",
                "price": 135000,
                "category": "Electronics",
                "is_sale": True,
                "sale_price": 115000,
                "image": "freepic1.jpg"
            },
            {
                "name": "Home Assistant",
                "description": "Smart home assistant with display",
                "price": 178000,
                "category": "Electronics",
                "is_sale": False,
                "sale_price": 178000,
                "image": "freepic2.jpg"
            }
        ]

        # Create sample images directory if it doesn't exist
        sample_images_dir = os.path.join(settings.MEDIA_ROOT, 'sample_images')
        os.makedirs(sample_images_dir, exist_ok=True)

        # Default image path
        default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_product.jpg')
        
        # Create products
        product_objects = []
        for product_data in products_data:
            # Create or get the product
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
            
            if created:
                # Use the specified image for the product
                image_name = product_data.get("image")
                if image_name:
                    # Try to find the image in multiple possible locations
                    possible_paths = [
                        os.path.join(settings.BASE_DIR, 'static', 'images', image_name),
                        os.path.join(settings.MEDIA_ROOT, 'sample_images', image_name),
                        os.path.join(settings.BASE_DIR, 'media', 'sample_images', image_name)
                    ]
                    
                    image_found = False
                    for image_path in possible_paths:
                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img_file:
                                product.image.save(
                                    image_name,
                                    ContentFile(img_file.read()),
                                    save=True
                                )
                            image_found = True
                            break
                    
                    if not image_found:
                        # Use default image if none of the specified images exist
                        default_image = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_product.jpg')
                        if os.path.exists(default_image):
                            with open(default_image, 'rb') as img_file:
                                product.image.save(
                                    'default_product.jpg',
                                    ContentFile(img_file.read()),
                                    save=True
                                )
                        else:
                            self.stdout.write(f"Warning: No image found for {product.name} and no default image available")
                
                self.stdout.write(f"Created product: {product.name}")
            
            product_objects.append(product)

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