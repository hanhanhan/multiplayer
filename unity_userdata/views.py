from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import Game_Session_Serializer
from .models import Game_Session


@api_view(['GET'])
def list_top_scoring_players(request, format=None):
	""" Top scoring players
	"""
	# How can this query can be done more efficiently?
	game_sessions = Game_Session.objects.order_by('points').reverse()[:10]
	serializer = Game_Session_Serializer(game_sessions, many=True)
	return Response(serializer.data)


# urg what is post vs put again?
class PlayerGameSession(APIView):
	""" Retrieve, update, or delete a player's game sessions.
	"""

	def get_object(self, player):
		# may be better to query on Player
		try:
			return Game_Session.objects.get(player=player)
		except Game_Session.DoesNotExist:
			raise Http404

	def get(self, request, player, format=None):
		game_session = self.get_object(player)
		serializer = Game_Session_Serializer(game_session)
		return Response(serializer.data)

	def put(self, request, player, format=None):
		game_session = self.get_object(player)
		serializer = Game_Session_Serializer(game_session, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, player, format=None):
		game_session = self.get_object(player)
		game_session.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
