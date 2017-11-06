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
		# Should I bother to take out the password below?
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
		# Database history? Prevent reuse of username? 
		request.user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class GameSessions(APIView):
	
	def get(self, request):
		# import pdb; pdb.set_trace()
		gamesessions = GameSession.objects.all()
		serializer = GameSessionSerializer(gamesessions, many=True)
		return Response(data=serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		pass



class PlayerGameSessions(APIView):

	def get(self, request):
		player_gamesessions = Player_GameSession.objects.all().filter(player=request.user)
		player_gamesdata = PlayerGameSessionSerializer(player_gamesessions)

		return Response(data=player_gamesdata)

	def put(self, request):
		pass


@api_view
def player_all_game_sessions(request):
	pass
# allow user to create, update, delete their game session info

# allow user to see all games available
# allower user to join game
# allow user to create game




class PlayerList(generics.ListAPIView):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer


class GameSessionList(APIView):
	# permission_classes = (permissions.IsAuthenticatedOrReadOnly)

	def get(self, request, format=None):
		game_sessions = GameSession.objects.all()
		serializer = GameSessionSerializer(game_sessions, many=True)
		return Response(serializer.data)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

	def post(self, request, format=None):
		serializer = GameSessionSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameSessionDetail(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly)
	def get_object(self, username):
		try:
			return GameSession.objects.get(username=username)
		except GameSession.DoesNotExist:
			raise Http404

	def get(self, request, username, format=None):
		game_session = self.get_object(username)
		serializer = GameSessionSerializer(game_session)

	def put(self, request, username, format=None):
		game_session = self.get_object(username)
		serializer = GameSessionSerializer(game_session)
		return Response(serializer.data)

	def delete(self, request, username, format=None):
		game_session = self.get_object(username)
		game_session.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	


# -------
@api_view(['POST'])
def create_player(request):
	username = request['username']
	email = request['email']
	Player.objects.create_user()

@api_view(['POST'])
def login(request):
	pass

@api_view()
def logout(request):
	pass

@api_view(['GET'])
def list_top_scoring_players(request, format=None):
	""" Top scoring players
	"""
	# How can this query can be done more efficiently?
	game_sessions = GameSession.objects.order_by('points').reverse()[:10]
	serializer = GameSessionSerializer(game_sessions, many=True)
	return Response(serializer.data)


class PlayerGameSession(APIView):
	""" Retrieve, update, or delete a player's game sessions.
	"""

	def get_object(self, player):
		# may be better to query on Player
		try:
			return GameSession.objects.get(player=player)
		except GameSession.DoesNotExist:
			raise Http404

	def get(self, request, player, format=None):
		game_session = self.get_object(player)
		serializer = GameSessionSerializer(game_session)
		return Response(serializer.data)

	def put(self, request, player, format=None):
		game_session = self.get_object(player)
		serializer = GameSessionSerializer(game_session, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, player, format=None):
		game_session = self.get_object(player)
		game_session.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

