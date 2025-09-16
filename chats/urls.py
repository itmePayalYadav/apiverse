from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.UserChatListView.as_view(), name="user-chats"),
    path("users/available/", views.AvailableUsersView.as_view(), name="available-users"),
    path("one-on-one/", views.OneOnOneChatView.as_view(), name="one-on-one-chat"),
    path("<uuid:pk>/", views.DeleteChatView.as_view(), name="delete-chat"),
    path("group/create/", views.GroupChatCreateView.as_view(), name="create-group-chat"),
    path("group/<uuid:pk>/", views.GroupChatDetailView.as_view(), name="group-chat-detail"),
    path("group/<uuid:pk>/update/", views.UpdateGroupChatNameView.as_view(), name="update-group-name"),
    path("group/<uuid:pk>/participant/add/", views.AddParticipantView.as_view(), name="add-participant"),
    path("group/<uuid:pk>/participant/remove/", views.RemoveParticipantView.as_view(), name="remove-participant"),
    path("group/<uuid:pk>/leave/", views.LeaveGroupChatView.as_view(), name="leave-group"),
    path("<uuid:pk>/messages/", views.ChatMessagesView.as_view(), name="chat-messages"),
    path("<uuid:pk>/send/", views.SendMessageView.as_view(), name="send-message"),
    path("messages/<uuid:pk>/", views.DeleteMessageView.as_view(), name="delete-message"),
    path("messages/<uuid:pk>/read/", views.MarkMessageAsReadView.as_view(), name="read-message"),
]