from django.test import TestCase
from django.urls import reverse
from apps.products.models import Product
from apps.common.models import ContactMessage
from apps.common.forms import ContactMessageForm


class IndexViewTests(TestCase):
    def setUp(self):
        for i in range(10):
            Product.objects.create(
                name=f'Product {i}',
                price=10 + i,
                sizes='M,L',
                description='Sample description',
                is_active=True
            )
    
    def test_index_view_status_code(self):
        response = self.client.get(reverse('common:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_context_contains_featured_products(self):
        response = self.client.get(reverse('common:index'))
        featured_products = response.context['featured_products']
        self.assertEqual(len(featured_products), 6) 

class AboutViewTests(TestCase):
    def test_about_view_status_code_and_template(self):
        response = self.client.get(reverse('common:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

class ContactViewTests(TestCase):
    def test_get_contact_view(self):
        response = self.client.get(reverse('common:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactMessageForm)

    def test_post_valid_contact_message(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Wonder',
            'email': 'alice@example.com',
            'subject': 'general',
            'message': 'Hello, I want to know more.'
        }
        response = self.client.post(reverse('common:contact'), data)
        self.assertRedirects(response, reverse('common:home'))
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.first_name, 'Alice')
        self.assertEqual(message.subject, 'general')

    def test_post_invalid_contact_message(self):
        data = {
            'first_name': 'Bob',
            'email': 'bob@example.com',
            'subject': 'general',
        }
        response = self.client.post(reverse('common:contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertEqual(ContactMessage.objects.count(), 0)