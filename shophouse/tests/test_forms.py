from django.test import TestCase
from shophouse.forms import BusinessRegistration, Productform
from django.core.files.uploadedfile import SimpleUploadedFile

class FormTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # empty image
            content_type='image/jpeg'
        )

    def test_business_registration_form_valid(self):
        """Test business registration form with valid data"""
        form_data = {
            'name_of_business': 'Test Business',
            'type_of_business': 'Retail',
            'email': 'test@business.com',
            'address': '123 Test St',
            'description': 'Test Description',
            'phone_number': '1234567890'
        }
        form = BusinessRegistration(data=form_data)
        self.assertTrue(form.is_valid())

    def test_business_registration_form_invalid(self):
        """Test business registration form with invalid data"""
        form_data = {
            'name_of_business': '',  # Required field
            'type_of_business': 'Retail',
            'email': 'invalid-email',  # Invalid email
            'address': '123 Test St',
            'phone_number': '123'  # Too short
        }
        form = BusinessRegistration(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_product_form_valid(self):
        """Test product form with valid data"""
        form_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 100,
            'is_sale': True,
            'sale_price': 80,
            'Category': 1
        }
        form_files = {
            'image': self.test_image
        }
        form = Productform(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid(self):
        """Test product form with invalid data"""
        form_data = {
            'name': '',  # Required field
            'price': 'not a number',  # Invalid price
            'sale_price': -10  # Negative price
        }
        form = Productform(data=form_data)
        self.assertFalse(form.is_valid())