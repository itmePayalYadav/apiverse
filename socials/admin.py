from django.contrib import admin

# Import models
from socials.models.profile import Profile
from socials.models.post import Post
from socials.models.comment import Comment
from socials.models.like import Like
from socials.models.bookmark import Bookmark
from socials.models.follow import Follow

# Register models
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(Follow)