from rest_framework import serializers
from .models import Game_Session, Player


class GameSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game_Session
		fields = ('id', 'player', 'x_position', 'y_position', 'level', 'points')


class Player_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = ('username', 'email', 'password')
