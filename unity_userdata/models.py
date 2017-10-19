from random import randint
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import UserManager


class Player(AbstractUser):
	# verify username is urlsave -- or change capture group/url displayed for user - or convert to utf8 for url
	username = models.CharField(max_length=40, unique=True, primary_key=True)
	email = models.EmailField(blank=False, unique=True)

	# Set django auth model to authenticate using email instead of username.
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	# objects = UserManager()

	def generate_confirmation_token(self, expiration=3600):
		pass

	def __str__(self):
		return f'Player {self.username}'

	@staticmethod
	def generate_fake(count=100):
		from faker import Faker
		fake = Faker()
		fake.seed_instance(1234)
		for player in range(count):
			player = Player()
			player.username = fake.word() + fake.word()
			player.email = fake.email()
			player.password = 'fake'
			player.is_active = True
			player.save()


class GameSession(models.Model):
	# or autokey incremented integer
	# I've seen people using 'id' in classes even though it's a keyword - bad? seems bad.
	game_session_id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	player = models.ManyToManyField(Player, through='GameSession_Player')

	def __str__(self):
		return f'Id {self.game_session_id}'

	@staticmethod
	def generate_fake(count=10):
		for session in range(count):
			game_session = GameSession()
			game_session.save()


class GameSession_Player(models.Model):
	# on_delete=models.Cascade -- I THINK this means if player is deleted, corresponding GameSession_Player entries are deleted
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	game_session = models.ForeignKey(GameSession, on_delete=None)
	# check range and type in unity
	x_position = models.BigIntegerField(default=0)
	y_position = models.BigIntegerField(default=0)
	points = models.PositiveIntegerField(default=0)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_accessed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Game Session {game_session.game_session_id} with player {player.username}'

	@staticmethod
	def generate_fake(count=100):
		for record in range(count):
			player = Player.objects.order_by('?').first()
			game_session = GameSession.objects.order_by('?').first()
			x_position = randint(-1000, 1000)
			y_position = randint(-1000, 1000)
			points = randint(0, 1000000)
			association = GameSession_Player(player=player, game_session=game_session, 
				x_position=x_position, y_position=y_position, points=points)
			association.save()

