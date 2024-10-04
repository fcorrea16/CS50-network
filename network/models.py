from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Like(models.Model):
    liked_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="liked_by")
    liked_post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="liked_post")
    liked = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "liked": self.liked,
            "liked post": self.liked_post.id
        }

    def __str__(self):
        return f"Post # {self.id} is liked = {self.liked} by {self.liked_by.username}"


class Post(models.Model):
    posted_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posted_by")
    post_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False, max_length=280)
    likes = models.ManyToManyField(Like, blank=True, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "post date": self.post_date.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
        }

    def __str__(self):
        return f"Post # {self.id} by {self.posted_by.username} on {self.post_date}"


# represent details about posts, likes, and followers.
