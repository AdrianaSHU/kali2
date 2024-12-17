from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Review


def home(request):
    return render(request, 'reviews/home.html')

def about(request):
    return render(request, 'reviews/about.html')

def contact(request):
    return render(request, 'reviews/contact.html')

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    return render(request, 'reviews/product_detail.html', {'product': product, 'reviews': reviews})

@login_required
def profile(request):
    return render(request, 'reviews/profile.html', {'profile': request.user.profile})

