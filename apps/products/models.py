from django.db import models
from apps.accounts.models import Profile

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Basketball Shoes'),
        ('apparel', 'Apparel'),
        ('equipment', 'Equipment'),
        ('accessories', 'Accessories'),
    ]

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    key_features = models.JSONField(blank=True, null=True)

    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sizes = models.JSONField(blank=True, null=True)  # example: ["S", "M", "L"]

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    
    title = models.CharField(max_length=255) 
    
    comment = models.TextField(blank=True, null=True)
    
    owned_duration_choices = [
        ('less-than-week', 'Less than a week'),
        ('1-2-weeks', '1-2 weeks'),
        ('1-month', 'About a month'),
        ('2-6-months', '2-6 months'),
        ('6-months-plus', '6+ months'),
        ('1-year-plus', 'Over a year'),
    ]
    owned_duration = models.CharField(
        max_length=20,
        choices=owned_duration_choices,
        blank=True,
        null=True,
    )
    
    recommend_choices = [
        ('definitely', 'Definitely'),
        ('probably', 'Probably'),
        ('maybe', 'Maybe'),
        ('probably-not', 'Probably not'),
        ('definitely-not', 'Definitely not'),
    ]
    recommend = models.CharField(
        max_length=20,
        choices=recommend_choices,
        blank=True,
        null=True,
    )
    
    pros = models.TextField(blank=True, null=True) 
    cons = models.TextField(blank=True, null=True)  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.profile}'