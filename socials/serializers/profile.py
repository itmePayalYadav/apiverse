from rest_framework import serializers
from socials.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("owner",)
    
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
    