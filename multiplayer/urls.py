from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from unity_userdata import views

urlpatterns = [
	url(r'^$', views.api_auth, name='get_token'),
	url(r'^new_player$', views.new_player, name='new_player'),
	url(r'^profile$', views.Profile.as_view(), name='profile'),
	url(r'^game-sessions$', views.GameSessions.as_view(), name='game_sessions'),
	url(r'^player-all-game-sessions$', views.player_all_game_sessions, name='player_all_game_sessions'),
	url(r'^player-game-session$', views.PlayerGameSession.as_view(), name='player_game_session'),
	url(r'^top-players$', views.list_top_scoring_players),
]

urlpatterns += [
	# url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
