from random import randint

from django.db import models
import uuid


class Game_Session(models.Model):
	# or autokey incremented integer
	id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	# look up behaviors for on_delete options
	player = models.ForeignKey('Player', related_name='game_sessions', on_delete=models.CASCADE)
	# check range and type in unity
	x_position = models.BigIntegerField()
	y_position = models.BigIntegerField()
	level = models.PositiveSmallIntegerField()
	points = models.PositiveIntegerField()
	last_accessed = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Player {self.player} in game session {self.id}'

	# need to look up how this is used
	class Meta:
		ordering = ('last_accessed',)

	@staticmethod
	def generate_fake(count=20):

		for session in range(count):
			player = Player()
			player.save()

			x_position = randint(-1000, 1000)
			y_position = randint(-1000, 1000)
			level = randint(1, 10)
			points = randint(0, 100000)

			game_session = Game_Session(player=player, x_position=x_position, y_position=y_position, level=level, points=points)
			game_session.save()


class Player(models.Model):
	pass
