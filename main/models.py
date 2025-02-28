from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f'{self.name}'

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.context[:30]}'
