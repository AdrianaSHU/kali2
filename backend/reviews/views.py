from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import InquiryForm, ReviewForm
from products.models import Product
from .models import Review


def home(request):
    products = Product.objects.all()
    return render(request, 'reviews/home.html', {'products': products})

def about(request):
    return render(request, 'reviews/about.html')

def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Prepare email content
            email_message = EmailMessage(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                email,  # From email
                [settings.DEFAULT_FROM_EMAIL],
            )
            email_message.content_subtype = 'html'
            email_message.send()

            # Show success message
            messages.success(request, 'Your inquiry has been sent!')

            # Redirect to the same contact page
            return redirect('/contact')  
    else:
        form = InquiryForm()

    return render(request, 'reviews/contact.html', {'form': form})

@login_required
def delete_review(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)
    
    # Ensure the user is the author of the review
    if review.author == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted!')
    else:
        messages.error(request, 'You are not authorized to delete this review.')

    return redirect('reviews:product_detail', product_id=product_id)

@login_required
def update_review(request, product_id, review_id):
    review = get_object_or_404(Review, id=review_id, product_id=product_id)
    
    # Ensure the user is the author of the review
    if review.author != request.user:
        messages.error(request, 'You are not authorized to edit this review.')
        return redirect('reviews:product_detail', product_id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('reviews:product_detail', product_id=product_id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/update_review.html', {
        'form': form,
        'product': Product.objects.get(id=product_id),
    })