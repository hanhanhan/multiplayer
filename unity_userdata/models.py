from random import randint
import uuid

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

dummy_password = 'fake'


# Signal to generate user token post-save
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Player(AbstractUser):
	# verify username is urlsave -- or change capture group/url displayed for user - or convert to utf8 for url
	username = models.CharField(max_length=40, unique=True)
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
			Player.objects
			player.username = fake.word() + fake.word()
			player.email = fake.email()
			player.set_password(dummy_password)
			player.is_active = True
			player.save()


class GameSession(models.Model):

	game_session_id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	player = models.ManyToManyField(Player, through='Player_GameSession')

	def __str__(self):
		return f'Id {self.game_session_id}'

	@staticmethod
	def generate_fake(count=10):
		for session in range(count):
			game_session = GameSession()
			game_session.save()


class Player_GameSession(models.Model):
	# on_delete=models.Cascade -- if player is deleted, corresponding GameSession_Player entries are deleted
	player = models.ForeignKey(Player, related_name='player_gamesession', on_delete=models.CASCADE)
	game_session = models.ForeignKey(GameSession, related_name='player_gamesession', on_delete=None)
	# check range and type in unity
	x_position = models.BigIntegerField(default=0)
	y_position = models.BigIntegerField(default=0)
	points = models.PositiveIntegerField(default=0)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_accessed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Game Session {self.game_session.game_session_id} with player {self.player.username}'

	@staticmethod
	def generate_fake(count=100):
		for record in range(count):
			player = Player.objects.order_by('?').first()
			game_session = GameSession.objects.order_by('?').first()
			x_position = randint(-1000, 1000)
			y_position = randint(-1000, 1000)
			points = randint(0, 1000000)
			association = Player_GameSession(player=player, game_session=game_session, 
				x_position=x_position, y_position=y_position, points=points)
			association.save()

