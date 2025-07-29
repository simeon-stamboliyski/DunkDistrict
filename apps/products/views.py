from django.views.generic import TemplateView
from django.shortcuts import render

class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'

def product_list_view(request):
    return render(request, 'product_list.html')

def review_form_view(request, pk):
    return render(request, 'review_form.html')