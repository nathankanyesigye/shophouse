from django.test import TestCase
from .models import Product, Categories, Profile, Customer, RegisterBusiness
# Create your tests here.


class ProductModelTest(TestCase):
    def test_product_model_exists(self):
        """Test that the product model exists"""
        self.assertTrue(Product)

class CategoriesModelTest(TestCase):       
    def test_categories_model_exists(self):
        """Test that the categories model exists"""
        self.assertTrue(Categories)
class ProfileModelTest(TestCase):       
    def test_product_model_exists(self):
        """Test that the profile model exists"""
        self.assertTrue(Profile)
class CustomerModelTest(TestCase):
    def test_product_model_exists(self):
        """Test that the customer model exists"""
        self.assertTrue(Customer)

class Registerbusiness(TestCase):
    def test_product_model_exists(self):
        """Test that the Register business model exists"""
        self.assertTrue(RegisterBusiness)
               
    
