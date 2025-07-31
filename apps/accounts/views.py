from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime

from .forms import RegisterForm, CustomLoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
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

def cart_view(request):
    return render(request, 'cart.html')

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