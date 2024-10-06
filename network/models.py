from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Like(models.Model):
    liked_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="liked_by")
    liked_post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="liked_post")

    def serialize(self):
        return {
            "id": self.id,
            "liked post": self.liked_post.id,
            "liked by": self.liked_by.id
        }

    def __str__(self):
        return f"#{self.id} - post {self.liked_post.id} is liked by {self.liked_by.username}"


class Post(models.Model):
    posted_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posted_by")
    post_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False, max_length=280)

    def serialize(self):
        return {
            "id": self.id,
            "post date": self.post_date.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
        }

    def __str__(self):
        return f"Post # {self.id} by {self.posted_by.username} on {self.post_date}"


class Followers(models.Model):
    pass

# represent details about posts, likes, and followers.
