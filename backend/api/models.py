from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Group(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User,through="GroupMember",related_name="groups")

class GroupMember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class PrivateChat(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)

class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)
