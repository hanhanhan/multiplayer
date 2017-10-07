from rest_framework import serializers
from .models import Game_Session


class Game_Session_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Game_Session
		fields = ('id', 'player', 'x_position', 'y_position', 'z_position', 'level', 'points')
		
