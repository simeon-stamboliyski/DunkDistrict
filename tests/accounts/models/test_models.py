from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile, Cart, Order, OrderItem
from apps.products.models import Product 

User = get_user_model()

class AccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')
        self.profile = Profile.objects.create(user=self.user, first_name="John", last_name="Doe")

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('securepassword123'))

    def test_profile_created(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.first_name, "John")
        self.assertEqual(str(self.profile), "John Doe")

    def test_cart_creation(self):
        cart = Cart.objects.create(profile=self.profile)
        self.assertEqual(str(cart), f"Cart for {self.profile}")

    def test_order_and_items(self):
        order = Order.objects.create(
            profile=self.profile,
            name="Order001",
            total_cost=100.00,
            status='pending'
        )

        product = Product.objects.create(name='Test Shoe', price=50.00, sizes='42,43', description='Cool shoe')
        order_item = OrderItem.objects.create(order=order, product=product, quantity=2)

        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order_item.price_at_order, 50.00)
        self.assertEqual(str(order_item), "2 x Test Shoe in order Order001")