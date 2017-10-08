from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from unity_userdata import views

urlpatterns = [
	url(r'^top-players$', views.list_top_scoring_players),
	url(r'^(?P<player>\d+)/game-session$', views.PlayerGameSession.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
