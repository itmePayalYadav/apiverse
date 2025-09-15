from django.urls import path
from socials import views

app_name = "socials"

urlpatterns = [
    # ----------------------
    # Profile Endpoints
    # ----------------------
    path("profile/", views.MyProfileView.as_view(), name="my_profile"),
    path("profile/update/", views.UpdateProfileView.as_view(), name="update_profile"),
    path("profile/cover-image/", views.UpdateCoverImageView.as_view(), name="update_cover_image"),
    path("profile/<str:username>/", views.ProfileByUsernameView.as_view(), name="profile_by_username"),

    # ----------------------
    # Post Endpoints
    # ----------------------
    path("posts/", views.PostListView.as_view(), name="list_posts"),
    path("posts/create/", views.PostCreateView.as_view(), name="create_post"),
    path("posts/<uuid:id>/", views.PostRetrieveView.as_view(), name="retrieve_post"),
    path("posts/<uuid:id>/update/", views.PostUpdateView.as_view(), name="update_post"),
    path("posts/<uuid:id>/delete/", views.PostDeleteView.as_view(), name="delete_post"),
    path("posts/me/", views.MyPostsView.as_view(), name="my_posts"),
    path("posts/user/<str:username>/", views.PostsByUsernameView.as_view(), name="posts_by_username"),
    path("posts/tag/<str:tag>/", views.PostsByTagView.as_view(), name="posts_by_tag"),
    path("posts/<uuid:post_id>/remove-image/", views.RemovePostImageView.as_view(), name="remove_post_image"),

    # ----------------------
    # Like / Unlike Endpoints
    # ----------------------
    path("posts/<uuid:post_id>/like/", views.LikePostView.as_view(), name="like_post"),
    path("comments/<uuid:comment_id>/like/", views.LikeCommentView.as_view(), name="like_comment"),

    # ----------------------
    # Comment Endpoints
    # ----------------------
    path("posts/<uuid:post_id>/comments/", views.PostCommentsView.as_view(), name="post_comments"),
    path("posts/<uuid:post_id>/comments/add/", views.AddCommentView.as_view(), name="add_comment"),
    path("comments/<uuid:comment_id>/update/", views.UpdateCommentView.as_view(), name="update_comment"),
    path("comments/<uuid:comment_id>/delete/", views.DeleteCommentView.as_view(), name="delete_comment"),

    # ----------------------
    # Bookmark Endpoints
    # ----------------------
    path("posts/<uuid:post_id>/bookmark/", views.BookmarkPostView.as_view(), name="bookmark_post"),
    path("bookmarks/me/", views.MyBookmarksView.as_view(), name="my_bookmarks"),

    # ----------------------
    # Follow / Unfollow Endpoints
    # ----------------------
    path("users/<uuid:user_id>/followers/", views.UserFollowersView.as_view(), name="user_followers"),
    path("users/<uuid:user_id>/following/", views.UserFollowingView.as_view(), name="user_following"),
    path("users/<uuid:user_id>/follow/", views.FollowUnfollowUserView.as_view(), name="follow_unfollow_user"),
]
