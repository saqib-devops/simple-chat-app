from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
    room_name = models.CharField(max_length=200000000)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
