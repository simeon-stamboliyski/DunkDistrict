from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile, Cart, CartItem, Order, OrderItem
from apps.products.models import Product

User = get_user_model()

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_email = 'testuser@example.com'
        self.user_password = 'TestPass123'
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password)
        self.profile = Profile.objects.create(user=self.user)
        self.product = Product.objects.create(name='Test Product', price=10.0, sizes='M,L')

    def test_register_view_post_success(self):
        response = self.client.post(reverse('accounts:register'), data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'date_of_birth': '1990-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='john@example.com').exists())

    def test_register_view_password_mismatch(self):
        response = self.client.post(reverse('accounts:register'), data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john2@example.com',
            'password': 'password123',
            'confirm_password': 'password456',
            'date_of_birth': '1990-01-01',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'confirm_password', 'Passwords do not match.')

    def test_login_view_success(self):
        response = self.client.post(reverse('accounts:login'), data={
            'username': self.user_email,
            'password': self.user_password,
        })
        self.assertRedirects(response, reverse('common:home'))

    def test_add_to_cart(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:add_to_cart'), data={
            'product_id': self.product.id,
            'quantity': '2',
            'size': 'M',
        })
        self.assertRedirects(response, reverse('accounts:cart'))
        cart = Cart.objects.get(profile=self.profile)
        cart_item = CartItem.objects.get(cart=cart, product=self.product, size='M')
        self.assertEqual(cart_item.quantity, 2)

    def test_update_quantity_increase(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(profile=self.profile)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, size='M', quantity=1)
        response = self.client.post(reverse('accounts:update_quantity', args=[cart_item.id]), data={'action': 'increase'})
        self.assertRedirects(response, reverse('accounts:cart'))
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(profile=self.profile)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, size='M', quantity=1)
        response = self.client.post(reverse('accounts:remove_from_cart', args=[cart_item.id]))
        self.assertRedirects(response, reverse('accounts:cart'))
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('accounts:profile')}")

        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('profile', response.context)

    def test_update_profile_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:update_profile'), data={
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'date_of_birth': '1985-05-15',
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        self.profile.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'NewFirst')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_checkout_creates_order_and_clears_cart(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(profile=self.profile)
        CartItem.objects.create(cart=cart, product=self.product, size='M', quantity=2)
        response = self.client.get(reverse('accounts:checkout'))
        self.assertRedirects(response, reverse('common:home'))
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.total_spent, 20.0)
        self.assertFalse(cart.items.exists())
        order = Order.objects.filter(profile=self.profile).last()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_cost, 20.0)
        self.assertEqual(order.items.count(), 1)