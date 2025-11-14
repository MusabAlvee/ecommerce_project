from django.shortcuts import render
from store.models import Product
# Create your views here.

def home(request):
    products = Product.objects.filter(is_available = True)
    return render(request, 'core/index.html', {
        'products': products
    })