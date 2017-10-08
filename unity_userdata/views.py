# from django.shortcuts import render, get_object_or_404
# from django.http import Http404, HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Game_Session_Serializer
from .models import Game_Session, Player


@api_view(['GET'])
def list_top_scoring_players(request, format=None):
	""" Top scoring players
	"""
	# How can this query can be done more efficiently?
	game_sessions = Game_Session.objects.order_by('points').reverse()[:10]
	serializer = Game_Session_Serializer(game_sessions, many=True)
	return Response(serializer.data)


# @csrf_exempt #only needed if post is defined w/o authentication
# urg what is post vs put again?
@api_view(['GET', 'POST'])
def player_game_session(request, player, format=None):
	# if request == 'GET':
	# may be better to query on Player
	game_session = Game_Session.objects.get(player=player)
	# rename class camelcase standard
	serializer = Game_Session_Serializer(game_session)
	return Response(serializer.data)
