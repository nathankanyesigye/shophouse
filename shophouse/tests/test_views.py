from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shophouse.models import Product, Categories, Profile
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