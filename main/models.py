from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    bio = models.TextField(max_length=300, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True)
    
    def __str__(self):
        return self.body

class Comment(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.body