from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        # If the user is created, create a profile for the user
        Profile.objects.create(user=instance)
    else:
        # If the user already exists, ensure their profile is saved
        if not hasattr(instance, 'profile'):
            # If the user doesn't have a profile yet, create one
            Profile.objects.create(user=instance)
        else:
            # Otherwise, save the existing profile
            instance.profile.save()
