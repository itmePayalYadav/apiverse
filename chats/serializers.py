from rest_framework import serializers
from .models import Chat, ChatMessage, MessageReadReceipt
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "content", "attachments", "created_at"]


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = ChatMessageSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "name", "is_group_chat", "last_message", "participants", "admin", "created_at", "is_active"]


class MessageReadReceiptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MessageReadReceipt
        fields = ["id", "message", "user", "read_at"]
