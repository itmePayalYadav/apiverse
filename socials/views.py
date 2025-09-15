from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from core.utils import api_response
from .models import Post, Profile, Bookmark, Comment, Follow
from .serializers import (
    PostSerializer, 
    ProfileSerializer, 
    CoverImageSerializer,
    LikeSerializer,
    CommentSerializer,
    BookmarkSerializer,
    FollowSerializer
)

# ==============================================================
#                       POST VIEWS
# ==============================================================

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
        image_url = request.data.get("image_url")

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


# ==============================================================
#                       PROFILE VIEWS
# ==============================================================

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

        serializer = self.get_serializer(
            profile,
            data={"cover_image": cover_image},
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            success=True,
            message="Cover image updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from socials.models import Post, Comment, Bookmark, Like, Follow, User
from socials.serializers import (
    LikeSerializer,
    CommentSerializer,
    BookmarkSerializer,
    FollowSerializer,
)

# ==============================================================
#                       LIKE VIEWS
# ==============================================================

class LikePostView(generics.GenericAPIView):
    """
    Like or unlike a post.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            liked_by=request.user, post=post
        )
        if not created:
            # Unlike if already liked
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)


class LikeCommentView(generics.GenericAPIView):
    """
    Like or unlike a comment.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = Like.objects.get_or_create(
            liked_by=request.user, comment=comment
        )
        if not created:
            like.delete()
            return Response({"message": "Comment unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Comment liked"}, status=status.HTTP_201_CREATED)


# ==============================================================
#                      COMMENT VIEWS
# ==============================================================

class PostCommentsView(generics.ListAPIView):
    """
    Get all comments for a specific post.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")


class AddCommentView(generics.CreateAPIView):
    """
    Add a new comment to a post.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)


class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"              
    lookup_url_kwarg = "comment_id"  

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class DeleteCommentView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


# ==============================================================
#                      BOOKMARK VIEWS
# ==============================================================

class MyBookmarksView(generics.ListAPIView):
    """
    Get all bookmarked posts of the authenticated user.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(bookmarked_by=self.request.user)


class BookmarkPostView(generics.GenericAPIView):
    """
    Add or remove a bookmark for a post.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(
            bookmarked_by=request.user, post=post
        )
        if not created:
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_200_OK)
        return Response({"message": "Post bookmarked"}, status=status.HTTP_201_CREATED)


# ==============================================================
#                       FOLLOW VIEWS
# ==============================================================

class UserFollowersView(generics.ListAPIView):
    """
    Get followers of a user.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)
        return Follow.objects.filter(followee=user)


class UserFollowingView(generics.ListAPIView):
    """
    Get users followed by a specific user.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)
        return Follow.objects.filter(follower=user)


class FollowUnfollowUserView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user, followee=user_to_follow 
        )
        if not created:
            follow.delete()
            return Response({"message": "Unfollowed user"}, status=status.HTTP_200_OK)
        return Response({"message": "Followed user"}, status=status.HTTP_201_CREATED)