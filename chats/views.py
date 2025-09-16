from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import Chat, ChatMessage, MessageReadReceipt
from .serializers import ChatSerializer, ChatMessageSerializer, UserSerializer, MessageReadReceiptSerializer
from core.utils import api_response

# ===========================
#   CHATS
# ===========================

# ----------------------
# List User Chats
# ----------------------
class UserChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            participants=self.request.user,
            is_active=True
        ).distinct()

    def list(self, request, *args, **kwargs):
        chats = self.get_queryset()
        serializer = self.get_serializer(chats, many=True)
        return api_response(
            success=True,
            message="Chats retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# List Available Users
# ----------------------
class AvailableUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
    
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return api_response(
            success=True,
            message="Available users retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Create/Get One-on-One Chat
# ----------------------
class OneOnOneChatView(generics.GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        other_user_id = request.data.get("user_id")
        if not other_user_id:
            return api_response(
                success=False,
                message="user_id is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        other_user = get_object_or_404(User, id=other_user_id)
        if other_user == request.user:
            return api_response(
                success=False,
                message="You cannot create a chat with yourself",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        chat = Chat.objects.filter(
            is_group_chat=False,
            participants=request.user,
            is_active=True
        ).filter(
            participants=other_user
        ).first()

        if not chat:
            chat = Chat.objects.create(
                name=f"Chat {request.user.username} & {other_user.username}",
                is_active=True
            )
            chat.participants.set([request.user, other_user])

        return api_response(
            success=True,
            message="One-on-one chat retrieved/created successfully",
            data=ChatSerializer(chat).data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Delete Chat
# ----------------------
class DeleteChatView(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        chat = get_object_or_404(self.get_queryset(), pk=kwargs["pk"], is_active=True)
        chat.delete()
        return api_response(
            success=True,
            message="Chat deleted successfully",
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Create Group Chat
# ----------------------
class GroupChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save(is_group_chat=True, admin=request.user)
        chat.participants.add(request.user)
        return api_response(
            success=True,
            message="Group chat created successfully",
            data=self.get_serializer(chat).data,
            status_code=status.HTTP_201_CREATED
        )

# ----------------------
# Group Chat Details
# ----------------------
class GroupChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(is_group_chat=True)
    
    def retrieve(self, request, *args, **kwargs):
        chat = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        return api_response(
            success=True,
            message="Group chat details retrieved successfully",
            data=self.get_serializer(chat).data,
            status_code=status.HTTP_200_OK
        )
        
# ----------------------
# Update Group Chat Name
# ----------------------
class UpdateGroupChatNameView(generics.UpdateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(is_group_chat=True)
    
    def update(self, request, *args, **kwargs):
        chat = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        serializer = self.get_serializer(chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Group chat updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Add Participant
# ----------------------
class AddParticipantView(generics.GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk, is_group_chat=True)
        user = get_object_or_404(User, id=request.data.get("user_id"))
        chat.participants.add(user)
        return api_response(
            success=True,
            message="Participant added successfully",
            data=ChatSerializer(chat).data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Remove Participant
# ----------------------
class RemoveParticipantView(generics.GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk, is_group_chat=True)
        user = get_object_or_404(User, id=request.data.get("user_id"))
        chat.participants.remove(user)
        return api_response(
            success=True,
            message="Participant removed successfully",
            data=ChatSerializer(chat).data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Leave Group Chat
# ----------------------
class LeaveGroupChatView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk, is_group_chat=True)
        chat.participants.remove(request.user)
        return api_response(
            success=True,
            message="You have left the group chat",
            status_code=status.HTTP_200_OK
        )

# ===========================
#   MESSAGES
# ===========================

# ----------------------
# Get All Messages of a Chat
# ----------------------
class ChatMessagesView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["pk"]
        return ChatMessage.objects.filter(chat_id=chat_id).order_by("created_at")
    
    def list(self, request, *args, **kwargs):
        message = self.get_queryset()
        serializer = self.get_serializer(message, many=True)
        
        return api_response(
            success=True,
            message="Messages retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        

# ----------------------
# Send a Message
# ----------------------
class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        chat_id = self.kwargs["pk"]
        chat = get_object_or_404(Chat, pk=chat_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user, chat=chat)
        
        chat.last_message = message
        chat.save(update_fields=["last_message"])
        
        return api_response(
            success=True,
            message="Message sent successfully",
            data=self.get_serializer(message).data,
            status_code=status.HTTP_201_CREATED
        )

# ----------------------
# Delete a Message
# ----------------------
class DeleteMessageView(generics.DestroyAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        message = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        message.delete()
        return api_response(
            success=True,
            message="Message deleted successfully",
            status_code=status.HTTP_200_OK
        )

# ===========================
#   READ RECEIPTS
# ===========================
class MarkMessageAsReadView(generics.CreateAPIView):
    serializer_class = MessageReadReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(ChatMessage, pk=pk)
        receipt, created = MessageReadReceipt.objects.get_or_create(
            message=message,
            user=request.user
        )
        return api_response(
            success=True,
            message="Message marked as read",
            data=self.get_serializer(receipt).data,
            status_code=status.HTTP_200_OK
        )