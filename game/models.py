from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)

class Board(models.Model):
    name = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
    )
    box = models.IntegerField(default=0)
    number = models.IntegerField(default=0)