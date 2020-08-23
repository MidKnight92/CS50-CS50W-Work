from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="user")
    post = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serializable(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }

    def __str__(self):
        return f"{self.user} wrote {self.post} on {self.timestamp}it has a post id of {self.id}. - end of post query"

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", default=None)
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee", default=None, null=True)

    class Meta:
        unique_together = (('user', 'followee'),)

    def serializable(self):
        return {
            "id": self.id,
            "follower": self.user,
            "followee": self.followee
        }

    def __str__(self):
        return f"Follower: {self.user} is following {self.followee} - end of follower query"
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True) 

    def serializable(self):
        return {
            "id": self.id,
            "post": self.post,
            "user": self.user
        }
    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return f"Liked by User:{self.user} post content {self.post} - end of like query"