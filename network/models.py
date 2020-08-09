from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="user")
    post = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveSmallIntegerField(default=0)

    def serializable(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }

    def __str__(self):
        return f"{self.user} wrote {self.post} on {self.timestamp}it has {self.likes} likes with a post id of {self.id}."

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey(User, on_delete=models.PROTECT, related_name="followee")
    liked_post = models.ForeignKey(Post, on_delete=models.PROTECT)

