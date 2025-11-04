from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shophouse.models import Product, Categories, Profile, RegisterBusiness
from cart.models import Cart, CartItem

class ViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Categories.objects.create(name="Electronics")
        self.product = Product.objects.create(
            Category=self.category,
            name="Test Product",
            description="Test Description",
            price=100,
            is_sale=False,
            sale_price=0
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue('products' in response.context)

    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(reverse('product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertEqual(response.context['product'], self.product)

    def test_cart_view(self):
        """Test cart view"""
        response = self.client.get(reverse('cart_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_summary.html')

    def test_login_view(self):
        """Test login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login

    def test_search_products_view(self):
        """Test product search functionality"""
        response = self.client.post(reverse('search'), {
            'searched': 'Test Product'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_protected_view_redirect(self):
        """Test that protected views redirect to login"""
        response = self.client.get(reverse('update_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/update_user/')

    def test_business_registration_view(self):
        """Test business registration and verification workflow"""
        # Login required for business registration
        self.client.login(username='testuser', password='12345')
        
        # Test business registration
        business_data = {
            'name_of_business': 'Test Business',
            'type_of_business': 'Retail',
            'email': 'test@business.com',
            'address': '123 Test St',
            'description': 'Test Description',
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('registerbusiness'), business_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        
        # Verify business was created with pending status
        business = RegisterBusiness.objects.get(name_of_business='Test Business')
        self.assertEqual(business.verification_status, 'pending')
        
        # Test adding product before verification (should fail)
        product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '100',
            'Category': self.category.id
        }
        response = self.client.post(reverse('addproduct'), product_data)
        self.assertEqual(response.status_code, 302)  # Should redirect with error