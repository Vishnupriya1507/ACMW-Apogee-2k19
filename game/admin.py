from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Player, Game, Board

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Board)