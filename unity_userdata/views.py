from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .serializers import Game_Session_Serializer
from .models import Game_Session, Player


# sort by points, high to low, top 10 results
def list_top_scoring_games(request):
	game_sessions = Game_Session.objects.all()
	serializer = Game_Session_Serializer(game_sessions, many=True)
	return JsonResponse(serializer.data, safe=False)


# @csrf_exempt #only needed if post is defined w/o authentication
def list_player_game_session(request, player):
	# if request == 'GET':
	game_session = Game_Session.objects.get(player=player)
	# rename class camelcase standard
	serializer = Game_Session_Serializer(game_session)
	return JsonResponse(serializer.data, safe=False)
