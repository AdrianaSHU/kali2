from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    # Check if the user is newly created
    if created:
        # Create the profile when a new user is created
        Profile.objects.create(user=instance)
    else:
        # Otherwise, save the user's profile if it already exists
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # If no profile exists, create one for the user
            Profile.objects.create(user=instance)

