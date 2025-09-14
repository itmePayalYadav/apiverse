from django.db import models
from accounts.models import User
from core.models import BaseModel

class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    class Meta:
        unique_together = ("follower", "followee")
    
    def __str__(self):
        return f"{self.follower} follows {self.followee}"
