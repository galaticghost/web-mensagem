from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Chat(models.Model):
    class ChatType(models.TextChoices):
        PRIVATE = "private","Private"
        GROUP = "group", "Group"
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20,choices=ChatType.choices)
    description = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ("chat", "user")

class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)

    class Meta:
        ordering = ["created_at"]
