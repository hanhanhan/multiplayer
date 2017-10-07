from django.db import models
import uuid


class Game(models.Model):
	# or autokey incremented integer
	game_id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	# look up on_delete options behaviors
	player = models.ForeignKey('Player', on_delete=models.CASCADE)
	# check range and type in unity
	x_position = models.BigIntegerField()
	y_position = models.BigIntegerField()
	level = models.PositiveSmallIntegerField()
	points = models.PositiveIntegerField()
	last_accessed = models.DateTimeField(auto_now=True, auto_now_add=True)


class Player(models.Model):
	pass
