from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.forms import RegisterForm, CustomLoginForm

class RegisterFormTests(TestCase):
    def test_valid_data_creates_user(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
            'date_of_birth': '2000-01-01',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'janesmith',
            'email': 'jane@example.com',
            'password': 'pass1',
            'confirm_password': 'pass2',
            'date_of_birth': '1990-01-01',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_missing_required_fields(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)

class CustomLoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_valid_login_with_username(self):
        form = CustomLoginForm(None, data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_login_wrong_password(self):
        form = CustomLoginForm(None, data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertFalse(form.is_valid())

    def test_invalid_login_nonexistent_user(self):
        form = CustomLoginForm(None, data={
            'username': 'ghost',
            'password': 'testpassword'
        })
        self.assertFalse(form.is_valid())