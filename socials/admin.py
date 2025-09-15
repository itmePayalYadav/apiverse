from django.contrib import admin
from .models import Post, Comment, Like, Bookmark, Follow, Profile

# Register models
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(Follow)