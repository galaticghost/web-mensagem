from django.db import models

class User(models.AbstractUser):
    pass

class Group(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)