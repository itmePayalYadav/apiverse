from rest_framework import serializers
from socials.models import Post
from socials.models import Comment
from socials.serializers.comment import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("author", "created_at", "updated_at")
