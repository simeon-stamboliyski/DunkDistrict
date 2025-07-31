from django.views.generic import TemplateView, FormView
from apps.products.models import Product
from .forms import ContactMessageForm
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:6]
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('common:home') 

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)