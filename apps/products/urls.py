from django.urls import path
from .views import ProductDetailView, product_list_view, review_form_view

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('', product_list_view, name='product_list'),
    path('<int:pk>/review/', review_form_view, name='review_form'),
]