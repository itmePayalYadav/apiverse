from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from socials.models.profile import Profile
from socials.serializers.profile import ProfileSerializer, CoverImageSerializer
from core.utils import api_response
from rest_framework.parsers import MultiPartParser, FormParser

# ----------------------
# Get My Profile
# ----------------------
class MyProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Profile, owner=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return api_response(
            success=True,
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Update My Profile
# ----------------------
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Profile, owner=self.request.user)
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Profile updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
# ----------------------
# Get Profile by Username
# ----------------------
class ProfileByUsernameView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    queryset = Profile.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get("username")
        profile = get_object_or_404(Profile, owner__username=username)
        serializer = self.get_serializer(profile)
        return api_response(
            success=True,
            message="Profile retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Update Cover Image
# ----------------------
class UpdateCoverImageView(generics.UpdateAPIView):
    serializer_class = CoverImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_object_or_404(Profile, owner=self.request.user)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        cover_image = request.FILES.get("cover_image")

        if not cover_image:
            return api_response(
                success=False,
                message="No cover image provided.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(profile, data={"cover_image": cover_image}, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            success=True,
            message="Cover image updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    