from django.test import TestCase
from apps.accounts.models import Profile
from apps.products.models import Product, Review
from apps.products.forms import ReviewForm

class ReviewFormTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            user_id=1,
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=99.99,
            categories='shoes',
            sizes=['S', 'M'],
        )

        self.valid_data = {
            'rating': 4,
            'title': 'Great Product!',
            'comment': 'Really liked this.',
            'owned_duration': Review.owned_duration_choices[3][0], 
            'recommend': Review.recommend_choices[0][0],   
            'pros': 'Comfortable and stylish',
            'cons': 'A bit pricey',
        }

    def test_form_valid_with_all_fields(self):
        form = ReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_required_fields(self):
        required_fields = ['rating', 'title', 'comment', 'owned_duration', 'recommend']
        for field in required_fields:
            data = self.valid_data.copy()
            data[field] = ''
            form = ReviewForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_rating_out_of_range(self):
        for invalid_rating in [0, 6, -1, 'a']:
            data = self.valid_data.copy()
            data['rating'] = invalid_rating
            form = ReviewForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn('rating', form.errors)

    def test_optional_fields_can_be_blank(self):
        data = self.valid_data.copy()
        data['pros'] = ''
        data['cons'] = ''
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())