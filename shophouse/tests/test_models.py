from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from shophouse.models import Product, Categories, Profile, Customer, RegisterBusiness
from decimal import Decimal

class CategoryTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.category = Categories.objects.create(name="Electronics")

    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.name, "Electronics")
        self.assertTrue(isinstance(self.category, Categories))
        self.assertEqual(str(self.category), "Electronics")

class ProductTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.category = Categories.objects.create(name="Electronics")
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # empty image
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            Category=self.category,
            name="Test Product",
            description="Test Description",
            price=100,
            image=self.test_image,
            is_sale=True,
            sale_price=80
        )

    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100)
        self.assertTrue(self.product.is_sale)
        self.assertEqual(self.product.sale_price, 80)
        self.assertEqual(str(self.product), "Test Product")

class ProfileTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.profile = Profile.objects.create(
            first_name="John",
            last_name="Doe",
            user_name="johndoe",
            email="john@example.com",
            password="testpass123",
            bio_data="Test bio"
        )

    def test_profile_creation(self):
        """Test profile creation"""
        self.assertEqual(self.profile.user_name, "johndoe")
        self.assertEqual(self.profile.email, "john@example.com")

class BusinessRegistrationTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.business = RegisterBusiness.objects.create(
            name_of_business="Test Business",
            type_of_business="Retail",
            email="business@example.com",
            address="123 Test St",
            description="Test Description",
            phone_number="1234567890"
        )

    def test_business_registration(self):
        """Test business registration"""
        self.assertEqual(self.business.name_of_business, "Test Business")
        self.assertEqual(self.business.type_of_business, "Retail")
        self.assertEqual(str(self.business), "Test Business")

    def test_business_fields_validation(self):
        """Test business fields validation"""
        self.assertEqual(len(self.business.phone_number), 10)
        self.assertTrue('@' in self.business.email)