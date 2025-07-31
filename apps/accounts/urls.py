from django.urls import path
from .views import register_view, login_view, ProfileView, cart_view, load_all_orders, update_profile, update_address
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', cart_view, name='cart'),
    path('load_all_orders/', load_all_orders, name='load_all_orders'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update-address/', update_address, name='update_address'),
]