from django.test import TestCase, Client
from django.urls import reverse
from cart.cart import Cart
from shophouse.models import Product, Categories

class CartTests(TestCase):
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

    def test_add_to_cart(self):
        """Test adding item to cart"""
        response = self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'productId': self.product.id
        })
        self.assertEqual(response.status_code, 200)
        
        # Check session
        session = self.client.session
        self.assertTrue('session_key' in session)

    def test_cart_update(self):
        """Test updating cart quantity"""
        # First add item to cart
        self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'productId': self.product.id
        })
        
        # Then update quantity
        response = self.client.post(reverse('cart:cart_update'), {
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_cart_remove(self):
        """Test removing item from cart"""
        # First add item to cart
        self.client.post(reverse('cart:cart_add'), {
            'action': 'post',
            'productId': self.product.id
        })
        
        # Then remove it
        response = self.client.get(reverse('cart:cart_delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_cart_summary(self):
        """Test cart summary page"""
        response = self.client.get(reverse('cart:cart_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_summary.html')