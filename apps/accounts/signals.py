from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile

@receiver(user_signed_up)
def create_profile_on_signup(request, user, **kwargs):
    print("[DEBUG] user_signed_up fired")
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        print(f"[DEBUG] Created profile for {user}")
    else:
        print(f"[DEBUG] Profile already exists for {user}")