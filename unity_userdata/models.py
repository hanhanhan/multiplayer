from random import randint
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import UserManager



class Player(AbstractUser):
	username = models.CharField(max_length=40, unique=True)
	email = models.EmailField(blank=False, unique=True, primary_key=True)
	confirmed = models.BooleanField(default=False)

	# Set django auth model to authenticate using email instead of username.
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	# objects = UserManager()

	def generate_confirmation_token(self, expiration=3600):
		pass

	# def __str__(self):
	# 	return f'Player {self.username}'

	@staticmethod
	def generate_fake(self, count=20):
		from faker import Faker
		fake = Faker()
		fake.seed_instance(1234)
		for player in range(count):
			player = Player()
			player.username = fake.word() + fake.word()
			player.email = fake.email()
			player.password = 'fake'
			player.save()


class GameSession(models.Model):
	# or autokey incremented integer
	game_session_id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	# look up behaviors for on_delete options
	player = models.ForeignKey('Player', related_name='game_sessions')
	# check range and type in unity
	x_position = models.BigIntegerField()
	y_position = models.BigIntegerField()
	level = models.PositiveSmallIntegerField()
	points = models.PositiveIntegerField()
	last_accessed = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Player {self.player} in game session {self.id}'

	@staticmethod
	def generate_fake(count=20):

		for session in range(count):
			# get random player from players in db
			for p in range(count):
				player = Player.objects.raw(
					'SELECT * FROM Player; ORDER BY RANDOM(); LIMIT 1'
				)
				# player = Player()
				# player.save()

				x_position = randint(-1000, 1000)
				y_position = randint(-1000, 1000)
				level = randint(1, 10)
				points = randint(0, 100000)

				game_session = Game_Session(player=player, x_position=x_position, y_position=y_position, level=level, points=points)
				game_session.save()



