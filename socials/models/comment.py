from django.db import models
from accounts.models import User
from core.models import BaseModel
from .post import Post

class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post.id}"