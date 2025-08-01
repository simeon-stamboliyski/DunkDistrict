from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import uuid
from decimal import Decimal

from .forms import RegisterForm, CustomLoginForm
from .models import Cart, CartItem, Order, OrderItem
from apps.products.models import Product

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('common:home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if 'remember' in request.POST:
                request.session.set_expiry(1209600) 
            else:
                request.session.set_expiry(0)
            
            return redirect('common:home')
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile

        context['orders'] = profile.orders.all().order_by('-created_at')[:3]
        context['orders_count'] = profile.orders.count()
        return context

@require_POST
@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    size = request.POST.get('size')

    if not all([product_id, quantity, size]):
        return HttpResponseBadRequest("Missing required fields.")

    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile
    quantity = int(quantity)

    cart, created = Cart.objects.get_or_create(profile=profile)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('accounts:cart')

@login_required
def cart_view(request):
    profile = request.user.profile
    cart, created = Cart.objects.get_or_create(profile=profile)
    cart_items = cart.items.select_related('product')

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 9.99 if cart_items else 0
    tax = round(subtotal * Decimal('0.08'), 2)
    total = round(subtotal + Decimal(shipping) + Decimal(tax), 2)

    context = {
        'cart_items': cart_items,
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__profile=request.user.profile)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        item.save()

    return redirect('accounts:cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__profile=request.user.profile)

    if request.method == 'POST':
        item.delete()

    return redirect('accounts:cart')

@login_required
def load_all_orders(request):
    profile = request.user.profile
    orders = profile.orders.all().order_by('-created_at')

    orders_data = []
    for order in orders:
        orders_data.append({
            'name': order.name,
            'total_cost': str(order.total_cost), 
            'created_at': localtime(order.created_at).strftime('%B %d, %Y'),
            'status': order.status,
        })

    return JsonResponse({'orders': orders_data})

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.last_name = request.POST.get('last_name', profile.last_name)
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        profile.phone = request.POST.get('phone', profile.phone)
        dob = request.POST.get('date_of_birth')
        if dob:
            profile.date_of_birth = dob
        profile.save()
        return redirect('accounts:profile')  

@login_required
def update_address(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.address = request.POST.get('address', profile.address)
        profile.country = request.POST.get('country', profile.country)
        profile.save()
        return redirect('accounts:profile')
    
@login_required
def checkout(request):
    profile = request.user.profile
    cart = profile.cart

    if not cart.items.exists():
        return redirect('accounts:cart')
    
    subtotal = sum(item.product.price * item.quantity for item in cart.items.all())
    shipping = 9.99 if cart.items else 0
    tax = round(subtotal * Decimal('0.08'), 2)
    total = round(subtotal + Decimal(shipping) + Decimal(tax), 2)

    order_name = f"ORDER-{uuid.uuid4().hex[:8].upper()}"

    order = Order.objects.create(
        profile=profile,
        name=order_name,
        total_cost=total,
        status='pending',
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_order=item.product.price,
        )

    profile.total_spent += total
    profile.save()

    cart.items.all().delete()

    return redirect('common:home')