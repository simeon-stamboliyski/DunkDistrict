from django.urls import path
from .views import register_view, login_view, ProfileView, cart_view, load_all_orders, update_profile, update_address, update_quantity, remove_from_cart, add_to_cart, checkout, cancel_order
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='common:home'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', cart_view, name='cart'),
    path('load_all_orders/', load_all_orders, name='load_all_orders'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update-address/', update_address, name='update_address'),
    path('update_quantity/<int:item_id>/', update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name="remove_from_cart"),
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    path('checkout/', checkout, name="checkout"),
    path("cancel-order/<int:order_id>/", cancel_order, name="cancel_order"),
]