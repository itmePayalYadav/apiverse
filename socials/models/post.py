from django.db import models
from django.utils import timezone
from accounts.models import User
from core.models import BaseModel

class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Post by {self.author}"

    def soft_delete(self): 
        """Mark the post as deleted instead of permanently removing it"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
