from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.products.models import Product, Review
from apps.accounts.models import Profile

class ProductViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.profile = Profile.objects.create(user=self.user)

        self.product = Product.objects.create(
            name='Test Shoe',
            description='Test shoe description',
            price=100,
            categories='shoes',
            sizes=['M', 'L'],
        )
        self.review = Review.objects.create(
            product=self.product,
            profile=self.profile,
            rating=5,
            title='Great',
            comment='Awesome product',
            owned_duration='1-month',
            recommend='definitely',
        )

    def test_product_detail_view(self):
        url = reverse('products:product_detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertIn('stars', response.context)
        self.assertIn('product', response.context)

    def test_product_list_view_filtering(self):
        url = reverse('products:product_list')
        response = self.client.get(url, {'q': 'Shoe', 'category': ['shoes'], 'size': ['M']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertIn('products', response.context)

    def test_review_form_get_requires_login(self):
        url = reverse('products:review_form', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  

        self.client.login(username='tester', password='pass1234')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('product', response.context)

    def test_review_form_post_creates_review(self):
        self.client.login(username='tester', password='pass1234')
        url = reverse('products:review_form', kwargs={'pk': self.product.pk})

        data = {
            'rating': 4,
            'title': 'Nice product',
            'comment': 'Really good',
            'owned_duration': '1-month',
            'recommend': 'definitely',
            'pros': 'Comfort',
            'cons': 'Pricey',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('products:product_detail', kwargs={'pk': self.product.pk}))
        self.assertTrue(Review.objects.filter(title='Nice product', profile=self.profile).exists())

    def test_delete_review_view_permission_and_delete(self):
        url = reverse('products:delete_review', kwargs={'review_id': self.review.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        other_user = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='tester', password='pass1234')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('products:product_detail', kwargs={'pk': self.product.pk}))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())