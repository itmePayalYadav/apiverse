from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from core.utils import api_response
from socials.models.post import Post
from socials.serializers.post import PostSerializer

# ----------------------
# List Posts
# ----------------------
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True).order_by("-created_at")
    
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return api_response(
            success=True,
            message="Posts retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Create Post
# ----------------------
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            success=True,
            message="Post created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

# ----------------------
# Retrieve Post
# ----------------------
class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True)
    
    def retrieve(self, request, *args, **kwargs):
        post = get_object_or_404(self.get_queryset(), id=kwargs["id"])
        serializer = self.get_serializer(post)
        return api_response(
            success=True,
            message="Post retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Update Post
# ----------------------
class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True, author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        post = get_object_or_404(self.get_queryset(), id=kwargs["id"])
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Post updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Delete Post 
# ----------------------
class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True, author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(self.get_queryset(), id=kwargs["id"])
        post.soft_delete()
        return api_response(
            success=True,
            message="Post deleted successfully",
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Get My Posts
# ----------------------
class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, deleted_at__isnull=True).order_by("-created_at")
    
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return api_response(
            success=True,
            message="My posts retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
# ----------------------
# Get Posts by Username
# ----------------------
class PostsByUsernameView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        username = self.kwargs.get("username")
        return Post.objects.filter(author__username=username, deleted_at__isnull=True).order_by("-created_at")
    
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return api_response(
            success=True,
            message=f"Posts by user '{self.kwargs['username']}' retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
# ----------------------
# Get Posts by Tag
# ----------------------
class PostsByTagView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        tag = self.kwargs.get("tag")
        return Post.objects.filter(tags__icontains=tag, deleted_at__isnull=True).order_by("-created_at")
    
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return api_response(
            success=True,
            message=f"Posts with tag '{self.kwargs['tag']}' retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
# ----------------------
# Remove Post Image
# ----------------------
class RemovePostImageView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id") 
        print(post_id)
        image_url = request.data.get("image_url")
        print(image_url)
        post = get_object_or_404(
            Post, id=post_id, author=request.user, deleted_at__isnull=True
        )
        
        if image_url not in post.images:
            return api_response(
                success=False,
                message="Image not found in this post",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        post.images.remove(image_url)
        post.save(update_fields=["images"])
        
        return api_response(
            success=True,
            message="Post image removed successfully",
            data=self.get_serializer(post).data,
            status_code=status.HTTP_200_OK
        )
        