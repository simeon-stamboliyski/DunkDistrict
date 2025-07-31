from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'categories')
    search_fields = ('name', 'description')
    list_filter = ('categories',)
    readonly_fields = ('id',)
    ordering = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'profile', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'recommend', 'owned_duration', 'created_at')
    search_fields = ('title', 'comment', 'pros', 'cons')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)