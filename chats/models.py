from django.db import models
from accounts.models import User
from core.models import BaseModel

class Chat(BaseModel):
    name = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    last_message = models.ForeignKey("ChatMessage",related_name="last_in_chat",on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="chats")
    admin = models.ForeignKey(User, related_name="admin_chats", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class ChatMessage(BaseModel):
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    attachments = models.JSONField(default=list, blank=True)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return f"Message by {self.sender} in {self.chat.name}"

class MessageReadReceipt(BaseModel):
    message = models.ForeignKey(ChatMessage, related_name="read_receipts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="read_messages", on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "user")  

    def __str__(self):
        return f"{self.user.username} read {self.message.id} at {self.read_at}"