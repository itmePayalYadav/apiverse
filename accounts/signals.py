from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from ecommerce.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile for a new User.
    Safe for superusers and handles required fields with defaults.
    """
    if created:
        Profile.objects.get_or_create(
            owner=instance,
            defaults={
                'first_name': instance.username,  
                'last_name': '',
                'country_code': '',
                'phone_number': ''
            }
        )