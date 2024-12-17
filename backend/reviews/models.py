from django.db import models
from django.contrib.auth.models import User

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

# Review Model
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    content = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} on {self.product.name}"
