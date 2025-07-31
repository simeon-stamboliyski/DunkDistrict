from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')

        product = get_object_or_404(Product, id=product_id)
        context['product'] = product
        context['stars'] = [1, 2, 3, 4, 5]
        return context

def product_list_view(request):
    products = Product.objects.all()

    q = request.GET.get('q', '')
    categories = request.GET.getlist('category')
    sizes = request.GET.getlist('size')

    if q:
        products = products.filter(name__icontains=q)
    if categories:
        products = products.filter(categories__in=categories)
    if sizes:
        from django.db.models import Q
        query = Q()
        for size in sizes:
            query |= Q(sizes__contains=[size])
        products = products.filter(query)

    context = {
        'products': products,
        'selected_categories': categories,  
        'selected_sizes': sizes,            
        'search_query': q,
    }
    return render(request, 'product_list.html', context)

@login_required
def review_form_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    profile = request.user.profile

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.profile = profile
            review.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'review_form.html', {
        'form': form,
        'product': product
    })


@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.profile.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == "POST":
        review.delete()
        return redirect('products:product_detail', pk=review.product.id)

    return render(request, 'confirm_delete.html', {'review': review})