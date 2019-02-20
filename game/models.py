from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.models import User
class PlayerUser(AbstractUser):
    name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null =True )

    score = models.IntegerField(default=0)
    face = models.IntegerField(default=0)   # oasis = 0, apogee = 1, blah blah = 2,blah blah = 3, blah blah = 4, blah blah = 5, blah blah = 6

    def __str__(self):
        return str(self.username)

class Game(models.Model):
    name = models.CharField(max_length=50)

class Board(models.Model):
    name = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
    )
    box = models.IntegerField(default=0)
    number = models.IntegerField(default=0)