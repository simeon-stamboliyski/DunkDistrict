from django.test import TestCase
from apps.products.forms import ReviewForm

class ReviewFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'rating': 4,
            'title': 'Excellent product',
            'comment': 'This product exceeded my expectations.',
            'owned_duration': '2-6 months', 
            'recommend': 'Definitely',             
            'pros': 'Easy to use, reliable',
            'cons': 'A bit expensive',
        }

    def test_form_valid_with_all_fields(self):
        form = ReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_without_optional_fields(self):
        data = self.valid_data.copy()
        data['pros'] = ''
        data['cons'] = ''
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_required_fields(self):
        required_fields = ['rating', 'title', 'comment', 'owned_duration', 'recommend']
        for field in required_fields:
            data = self.valid_data.copy()
            data[field] = ''
            form = ReviewForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_rating_field_accepts_only_valid_choices(self):
        for invalid_rating in [0, 6, -1, 'a', None]:
            data = self.valid_data.copy()
            data['rating'] = invalid_rating
            form = ReviewForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn('rating', form.errors)

        for valid_rating in range(1, 6):
            data = self.valid_data.copy()
            data['rating'] = valid_rating
            form = ReviewForm(data=data)
            self.assertTrue(form.is_valid())

    def test_widgets_have_correct_css_classes(self):
        form = ReviewForm()
        self.assertIn('form-control-custom', str(form['title']))
        self.assertIn('form-control-custom', str(form['comment']))
        self.assertIn('form-control-custom', str(form['owned_duration']))
        self.assertIn('form-control-custom', str(form['recommend']))
        self.assertIn('form-control-custom', str(form['pros']))
        self.assertIn('form-control-custom', str(form['cons']))
        self.assertIn('type="radio"', str(form['rating']))

    def test_rating_choices_labels(self):
        form = ReviewForm()
        expected_choices = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
        self.assertEqual(form.fields['rating'].choices, expected_choices)