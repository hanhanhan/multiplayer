from rest_framework import serializers
from .models import GameSession, Player


class GameSessionSerializer(serializers.ModelSerializer):
	player = serializers.ReadOnlyField(source='player.username')
	
	class Meta:
		model = GameSession
		fields = ('game_session_id', 'player', 'x_position', 'y_position', 'level', 'points')


class PlayerSerializer(serializers.ModelSerializer):
	game_sessions = serializers.PrimaryKeyRelatedField(many=True, queryset=GameSession.objects.all())	
	
	class Meta:
		model = Player
		fields = ('email', 'username', 'game_sessions')