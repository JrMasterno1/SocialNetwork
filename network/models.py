from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey, ManyToManyField


class User(AbstractUser):
    pass
class Post(models.Model):
    content = models.CharField(max_length=500)
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    date = models.DateTimeField()
    like = models.IntegerField()
    def __str__(self):
        return f"${self.content}"
class User_Post_like(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
class Comment(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    content = models.CharField(max_length=100)
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
