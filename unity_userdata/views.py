from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response 

# token = Token.objects.create(user=...)
# http://www.tomchristie.com/rest-framework-2-docs/api-guide/authentication#basicauthentication
# For clients to authenticate, the token key should be included in the Authorization HTTP header. 
# The key should be prefixed by the string literal "Token", with whitespace separating the two strings. 
# For example:

from .serializers import GameSessionSerializer, PlayerSerializer
from .models import GameSession, Player

# -------
""" Views needed:
Name - Permissions - URL

Player - 

"""
# ------- 
def home(request):
	return Response({'hello':'home page'})


@api_view(['GET', 'POST'])
def player_account(request):
	import pdb; pdb.set_trace()
	if request.method == 'GET':
		player = get_object_or_404(Player, username=request.user)

	player_serializer = PlayerSerializer(player) 
	
	return Response(player_serializer.data)


# class PlayerAccount(generics.RetrieveAPIView, LoginRequiredMixin, UserPassesTestMixin):
# 	# For LoginRequiredMixin:
# 	login_url = '/login/'
# 	redirect_field_name = 'redirect_to'
# 	authentication_classes = (TokenAuthentication, BasicAuthentication)
# 	permission_classes = (IsAuthenticated)


# 	# For UserPassesTestMixin:
# 	def test_func(self):
# 		# check user is logged in
# 		return True
	
# 	# def get(self):
# 	# 	pass



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

