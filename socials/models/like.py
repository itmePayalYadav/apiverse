from django.db import models
from accounts.models import User
from core.models import BaseModel
from .post import Post
from .comment import Comment

class Like(BaseModel):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    
    def __str__(self):
        target = self.post if self.post else self.comment
        return f"{self.liked_by} liked {target}"