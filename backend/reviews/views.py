from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import InquiryForm, ReviewForm
from products.models import Product
from .models import Review
import requests
import os


def home(request):
    # Get all products
    products = Product.objects.all()

    # Weather API data
    url_template = 'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
    cities = [('Doncaster', 'UK'), ('Namche Bazar', 'Nepal'), ('Cancun', 'Mexico'), ('Yakutsk', 'Russia'), ('New York', 'US'), ('Canterbury', 'UK')]
    weather_data = []
    api_key = settings.WEATHER_API_KEY

    for city, country in cities:
        try:
            # Format the URL for each city and make the request
            url = url_template.format(city=city, country=country, api_key=api_key)  # Don't overwrite the original `url_template`
            response = requests.get(url)
            if response.status_code == 200:  # Check if the request was successful
                city_weather = response.json()  # Convert the JSON response to a dictionary

                # Add the weather data to the list
                weather = {
                    'city': f"{city_weather['name']}, {city_weather['sys']['country']}",
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                }
                weather_data.append(weather)
            else:
                print(f"Failed to fetch data for {city}, {country}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data for {city}, {country}: {e}")

    # Pass both weather data and products to the template
    return render(request, 'reviews/home.html', {
        'title': 'Homepage',
        'weather_data': weather_data,
        'products': products
    })

def about(request):
    return render(request, 'reviews/about.html')

def contact(request):
    """Handle contact form submissions, send emails, and save a record of emails to the configured path."""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            try:
                # Prepare and send the email
                email_message = EmailMessage(
                    subject,
                    f"Message from {name} ({email}):\n\n{message}",
                    email,  # From email
                    [settings.DEFAULT_FROM_EMAIL],
                )
                email_message.content_subtype = 'html'
                email_message.send()

                # Save the email to the file path specified in settings
                email_log_path = settings.EMAIL_LOG_PATH
                os.makedirs(email_log_path, exist_ok=True)  # Ensure the directory exists
                
                with open(os.path.join(email_log_path, "contact_emails.txt"), "a") as email_log_file:
                    email_log_file.write(
                        f"Subject: {subject}\n"
                        f"From: {name} <{email}>\n"
                        f"Message:\n{message}\n"
                        f"{'-'*50}\n"
                    )
                
                # Show success message
                messages.success(request, 'Your inquiry has been sent and saved!')
                return redirect(reverse('reviews:contact'))
            
            except Exception as e:
                # Handle email sending or file errors
                messages.error(request, f"An error occurred while processing your inquiry: {str(e)}")
        else:
            messages.error(request, "There was an error in your form submission.")
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
