from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from reviews.forms import ReviewForm
from django.contrib import messages

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.product = product
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('reviews:product_detail', product_id=product.id) 
    else:
        form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


def product_list(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})