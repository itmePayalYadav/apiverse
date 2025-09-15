from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from accounts.models import User
from core.models import BaseModel

# ==============================================================
#                            POST
# ==============================================================
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


# ==============================================================
#                           COMMENT
# ==============================================================
class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.post.id}"


# ==============================================================
#                            LIKE
# ==============================================================
class Like(BaseModel):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)

    def __str__(self):
        target = self.post if self.post else self.comment
        return f"{self.liked_by} liked {target}"


# ==============================================================
#                          BOOKMARK
# ==============================================================
class Bookmark(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    bookmarked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        unique_together = ("post", "bookmarked_by")

    def __str__(self):
        return f"{self.bookmarked_by} bookmarked {self.post.id}"


# ==============================================================
#                           FOLLOW
# ==============================================================
class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ("follower", "followee")

    def __str__(self):
        return f"{self.follower} follows {self.followee}"


# ==============================================================
#                           PROFILE
# ==============================================================
PLACEHOLDER_COVER_URL = "https://dummyimage.com/800x450/000/fff&text={name}+Cover"

class Profile(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_profile")
    first_name = models.CharField(max_length=30, default="John")
    last_name = models.CharField(max_length=30, default="Doe")
    bio = models.TextField(blank=True, default="")
    dob = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, default="")
    country_code = models.CharField(max_length=5, blank=True, default="")
    phone_number = models.CharField(max_length=20, blank=True, default="")
    cover_image = models.ImageField(upload_to="profile/covers/", blank=True, null=True)

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
