from django.db import models
from django.utils.functional import cached_property
from accounts.models import User
from core.models import BaseModel

PLACEHOLDER_COVER_URL = "https://dummyimage.com/800x450/000/fff&text={name}+Cover"

class Profile(BaseModel):
    owner: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="social_profile"
    )
    first_name: models.CharField = models.CharField(max_length=30, default="John")
    last_name: models.CharField = models.CharField(max_length=30, default="Doe")
    bio: models.TextField = models.TextField(blank=True, default="")
    dob: models.DateField = models.DateField(blank=True, null=True)
    location: models.CharField = models.CharField(max_length=100, blank=True, default="")
    country_code: models.CharField = models.CharField(max_length=5, blank=True, default="")
    phone_number: models.CharField = models.CharField(max_length=20, blank=True, default="")
    cover_image: models.ImageField = models.ImageField(
        upload_to="profile/covers/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["owner__username"] 

    def __str__(self) -> str:
        return f"{self.owner.username}'s profile"

    # ----------------------------
    # Cover Image URL
    # ----------------------------
    @cached_property
    def cover_image_url(self) -> str:
        """
        Returns the URL of the uploaded cover image.
        If not uploaded, returns a dynamic placeholder URL.
        """
        if self.cover_image and hasattr(self.cover_image, "url"):
            try:
                return self.cover_image.url
            except ValueError:
                pass
        name = self.owner.username.replace(" ", "+")
        return PLACEHOLDER_COVER_URL.format(name=name)
