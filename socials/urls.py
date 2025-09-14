from django.urls import path
from socials.views import profile, post

app_name = "socials"

urlpatterns = [
    # ----------------------
    # Profile Endpoints
    # ----------------------
    path("profile/", profile.MyProfileView.as_view(), name="my_profile"),
    path("profile/update/", profile.UpdateProfileView.as_view(), name="update_profile"),
    path("profile/cover-image/", profile.UpdateCoverImageView.as_view(), name="update_cover_image"),
    path("profile/<str:username>/", profile.ProfileByUsernameView.as_view(), name="profile_by_username"),

    # ----------------------
    # Post Endpoints
    # ----------------------
    path("posts/", post.PostListView.as_view(), name="list_posts"),
    path("posts/create/", post.PostCreateView.as_view(), name="create_post"),
    path("posts/<uuid:id>/", post.PostRetrieveView.as_view(), name="retrieve_post"),
    path("posts/<uuid:id>/update/", post.PostUpdateView.as_view(), name="update_post"),
    path("posts/<uuid:id>/delete/", post.PostDeleteView.as_view(), name="delete_post"),
    path("posts/me/", post.MyPostsView.as_view(), name="my_posts"),
    path("posts/user/<str:username>/", post.PostsByUsernameView.as_view(), name="posts_by_username"),
    path("posts/tag/<str:tag>/", post.PostsByTagView.as_view(), name="posts_by_tag"),
    path("posts/<uuid:post_id>/remove-image/", post.RemovePostImageView.as_view(), name="remove-post-image")
]
