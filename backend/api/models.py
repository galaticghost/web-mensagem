from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Group(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)