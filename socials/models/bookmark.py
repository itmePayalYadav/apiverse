from django.db import models
from accounts.models import User
from core.models import BaseModel
from .post import Post

class Bookmark(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    bookmarked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        unique_together = ("post", "bookmarked_by")
    
    def __str__(self):
        return f"{self.bookmarked_by} bookmarked {self.post.id}"