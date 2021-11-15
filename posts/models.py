from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='Posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
