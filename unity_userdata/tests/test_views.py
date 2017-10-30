from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase, Client
from django.utils.html import escape
from rest_framework.authtoken.models import Token

from unity_userdata import views
from unity_userdata.models import Player, GameSession, Player_GameSession, dummy_password




class PlayerLoginTest(TestCase):
    pass


class PlayerSettingsTest(TestCase):
    def setUp(self):
        self.aleph_player = Player()
        self.aleph_player.email = 'abe@astronomy.aa'
        self.aleph_player.username = 'abelincoln'
        self.aleph_player.save()

        self.bet_player = Player()
        self.bet_player.email = 'bee@blob.bb'
        self.bet_player.username = 'bebovaldes'
        self.bet_player.save()
        
        self.game_session = GameSession()
        self.game_session.save()
        self.player_game_session = Player_GameSession.objects.create(game_session=self.game_session, player=self.aleph_player)
        
    def test_login(self):
        pass
        

    def test_player_views_own_account_on_GET(self):
        client = Client()
        client.force_login(self.aleph_player)
        
        response = client.get('/')
        import ipdb; ipdb.set_trace()


    def test_player_POST_doesnt_post_others_settings(self):
        pass

    def test_player_POST_updates_own_email(self):
        pass

