from rest_framework import serializers
from .models import Post, Comment, Like, Bookmark, Follow, Profile

# ==============================================================
#                           COMMENT SERIALIZER
# ==============================================================
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['id', 'author', 'post', 'created_at', 'updated_at']


# ==============================================================
#                           POST SERIALIZER
# ==============================================================
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("author", "created_at", "updated_at")


# ==============================================================
#                           LIKE SERIALIZER
# ==============================================================
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ("liked_by",)


# ==============================================================
#                           BOOKMARK SERIALIZER
# ==============================================================
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = ("bookmarked_by",)


# ==============================================================
#                           FOLLOW SERIALIZER
# ==============================================================
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("follower",)


# ==============================================================
#                           PROFILE SERIALIZER
# ==============================================================
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("owner",)


# ----------------------
# Cover Image Serializer
# ----------------------
class CoverImageSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["cover_image", "cover_image_url"]

    def get_cover_image_url(self, obj):
        request = self.context.get("request")
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None
