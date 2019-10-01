from django.db import models


class Player(models.Model):
    pass


class Game(models.Model):
    is_ended = models.BooleanField(default=False)
    number = models.IntegerField()


class PlayerGameInfo(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
