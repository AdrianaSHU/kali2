from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review)
def review_created(instance, created, **_):
    if created:
        print(f"A new review was created for the product {instance.product.name}.")