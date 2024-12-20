from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True, default='/product_photos/default-image.jpg')

    def __str__(self):
        return self.name