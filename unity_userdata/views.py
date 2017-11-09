# TODO:
# consider updating gets -> post
# check all players are returned for game_session play

import logging

from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer 

from .serializers import GameSessionSerializer, PlayerSerializer, PlayerGameSessionSerializer
from .models import GameSession, Player, Player_GameSession

logger = logging.getLogger(__name__)

# Default REST_FRAMEWORK authentications and permissions are in in settings.py
# access to unrestricted endpoints must be whitelisted by setting permission, authentication by view

@api_view(['POST'])
@permission_classes(())
@authentication_classes(())
def api_auth(request):
	""" Post username/password to get token. Whitelisted endpoint.
	"""
	username = request.data.get('username', None)
	password = request.data.get('password', None)

	if password is None or username is None:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	try:
		player = Player.objects.get(username=username)
	except DoesNotExist:
		return Response(status=status.HTTP_401_UNAUTHORIZED) 
	
	if player.check_password(password):
		# better practice - generate new token
		data = {'token': player.auth_token.key}
		return Response(data=data)

	return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes(()) 
@authentication_classes(())
def new_player(request):
	player_serializer = PlayerSerializer(data=request.data)
	if player_serializer.is_valid():
		player_serializer.save()
		# QUESTION: Should I bother to take out the password below?
		data = player_serializer.data.pop('password')
		return Response(player_serializer.data, status=status.HTTP_201_CREATED)
	else:
		logger.error(f'New player creation error. POST data: {request.data}, Player Serializer errors: {player_serializer.errors}')
		return Response(status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):

	def get(self, request):
		player_serializer = PlayerSerializer(request.user, context={'request': request}) 
		data = player_serializer.data
		return Response(data=data)

	def post(self, request):	
		player = request.user
		serializer = PlayerSerializer(player, data=request.data, partial=True)
		if serializer.is_valid():
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		else:
			logger.error(f'Player update error. POST data: {request.data}, Player Serializer errors: {player_serializer.errors}')
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		logger.info(f'User deleted. Username: {request.user.username} Email: {request.user.email}')
		# QUESTION: Is this tracked in database history? Prevent reuse of username in database or here? 
		request.user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class GameSessions(APIView):
	
	def get(self, request):
		""" See all game sessions available.
		"""
		gamesessions = GameSession.objects.all()
		serializer = GameSessionSerializer(gamesessions, many=True)
		return Response(data=serializer.data, status=status.HTTP_200_OK)


	def post(self, request):
		""" Individual player joins game session with default start values. 
		"""
		game_session = GameSession.objects.create()
		player_gamesession = Player_GameSession(player=request.user, game_session=game_session)
		serializer = PlayerGameSessionSerializer(player_gamesession)
		return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def player_all_game_sessions(request):
	""" See all game sessions a player belongs to.
	"""
	player__game_sessions = Player_GameSession.objects.all().filter(player=request.user)
	serializer = PlayerGameSessionSerializer(player__game_sessions, many=True)
	return Response(data=serializer.data, status=status.HTTP_200_OK)


class PlayerGameSession(APIView):

	def post(self, request):
		""" See all players in game session.
		"""
		game_session = request.data['game_session']
		game_session_all_players = Player_GameSession.objects.all().filter(game_session=game_session)
	
		serializer = PlayerGameSessionSerializer(game_session_all_players, many=True)
		return Response(data=serializer.data, status=status.HTTP_200_OK)


	def put(self, request):
		""" Update individual player's game play in game session.
		"""
		game_session = request.data['game_session']
		data = {}
		data['x_position'] = request.data['x_position']
		data['y_position'] = request.data['y_position']
		data['points'] = request.data['points']
		player__game_session = Player_GameSession.objects.get(game_session=game_session, player=request.user)
		serializer = PlayerGameSessionSerializer(player__game_session, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
		else:
			logger.error(f'Update error for player\'s game session. PUT data: {request.data}, PlayerGameSessionSerializer errors: {serializer.errors}')
			return Response(status=status.HTTP_400_BAD_REQUEST)


	def delete(self, request):
		""" Remove individual player from game.
		"""
		game_session = request.data['game_session']
		player__game_session = Player_GameSession.objects.all().filter(game_session=game_session, player=request.user)
		logger.info(f'Player\'s game session deleted. Username: {request.user.username} from {game_session}')
		player__game_session.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_top_scoring_players(request, format=None):
	""" Top scoring players
	"""
	# QUESTION: How can this query can be done more efficiently?
	game_sessions = GameSession.objects.order_by('points').reverse()[:10]
	serializer = GameSessionSerializer(game_sessions, many=True)
	return Response(serializer.data)


