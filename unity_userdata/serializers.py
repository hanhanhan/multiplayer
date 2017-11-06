from rest_framework import serializers
from .models import GameSession, Player, Player_GameSession


class GameSessionSerializer(serializers.ModelSerializer):
	player = serializers.ReadOnlyField(source='player.username')
	
	class Meta:
		model = GameSession
		fields = '__all__'


class PlayerGameSessionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player_GameSession
		fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
	# player_gamesession = serializers.HyperlinkedRelatedField(
	# 	many=True, 
	# 	read_only=True, 
	# 	view_name='player_gamesession')

	class Meta:
		model = Player
		fields = ('email', 'username', 'password')


