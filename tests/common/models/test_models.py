from django.test import TestCase
from apps.common.models import ContactMessage
from apps.common.forms import ContactMessageForm

class ContactMessageModelTest(TestCase):
    def test_create_contact_message(self):
        msg = ContactMessage.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            subject="product",
            message="I have a question about your product."
        )
        self.assertEqual(str(msg), "John Doe - product")
        self.assertEqual(msg.subject, "product")
        self.assertIsNotNone(msg.created_at)

class ContactMessageFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'first_name': "Jane",
            'last_name': "Smith",
            'email': "jane@example.com",
            'subject': "order",
            'message': "Where is my order?"
        }
        form = ContactMessageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        data = {
            'first_name': "Jane",
            'email': "jane@example.com",
            'subject': "order",
        }
        form = ContactMessageForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertIn('message', form.errors)

    def test_invalid_subject_choice(self):
        data = {
            'first_name': "Jake",
            'last_name': "Peralta",
            'email': "jake@example.com",
            'subject': "invalid_choice",
            'message': "Testing invalid subject"
        }
        form = ContactMessageForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)