from django.db import models
from django.contrib.auth.models import AbstractUser
class Game(models.Model):
    name = models.CharField(max_length=50)

class Board(models.Model):
    name = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
    )
    box = models.IntegerField(default=0)
    number = models.IntegerField(default=0)

class User_Profile(models.Model):
    user_name = models.CharField(max_length=20)
    age = models.IntegerField()
    password = models.CharField(max_length = 30)
    user_score = models.IntegerField(default= 0, null=True)
    def __str__(self):
		return self.username