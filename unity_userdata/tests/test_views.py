import json
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.utils.html import escape
from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
import requests

from unity_userdata import views
from unity_userdata.models import Player, GameSession, Player_GameSession


class PlayerSettingsTest(TestCase):

    def setUp(self):
        self.player_alpha = Player()
        self.player_alpha.email = 'abe@astronomy.aa'
        self.player_alpha.set_password('fake_a')
        self.player_alpha.username = 'abelincoln'
        self.player_alpha.save()

        self.player_beta = Player()
        self.player_beta.email = 'bee@blob.bb'
        self.player_beta.set_password('fake_b')
        self.player_beta.username = 'bebovaldes'
        self.player_beta.save()
        
        self.game_session = GameSession()
        self.game_session.save()
        self.player_gamesession = Player_GameSession.objects.create(game_session=self.game_session, player=self.player_alpha)

        self.client_player_a = Client(HTTP_AUTHORIZATION=f'Token {self.player_alpha.auth_token.key}')
        self.profile_url = reverse('profile')

    def test_token_retrieval(self):
        client = Client()
        token_endpoint = reverse('get_token')

        unauth_response = client.post(token_endpoint, {
            'username': self.player_alpha.username, 
            'password': 'not right'
            })
        self.assertEqual(unauth_response.status_code, 401)

        response = client.post(token_endpoint, {
            'username': self.player_alpha.username, 
            'password': 'fake_a'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.player_alpha.auth_token.key)
         
        
    def test_new_player_POST_can_create_new_player_on_valid_request(self):
        client = Client()
        url = reverse('new_player')

        email = 'test_new_player@localhost.com'
        username = 'NewPlayr'
        data = {'email':email, 'username':username, 'password':'fake'}
        json_data = json.dumps(data)
        response = client.post(path=url, data=json_data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)

        queried_player = Player.objects.get(username=username)
        self.assertEqual(queried_player.email, email)

        incomplete_data = data.pop('email')
        incomplete_json_data = json.dumps(incomplete_data)
        response = client.post(path=url, data=incomplete_json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_player_views_own_account_with_valid_token_only_on_GET(self):  
        auth_token = f'Token {self.player_alpha.auth_token.key}'
        client = Client()

        invalid_token = 'Token not_a_valid_token'
        response = self.client.get(self.profile_url, HTTP_AUTHORIZATION=invalid_token)
        self.assertEqual(response.status_code, 401)
        
        response = self.client.get(self.profile_url, HTTP_AUTHORIZATION=auth_token)
        self.assertEqual(response.status_code, 200)


    def test_player_can_delete_account(self): 
        response = self.client_player_a.delete(self.profile_url)
        self.assertEqual(response.status_code, 204)


    def test_player_POST_updates_profile_info(self):
        username = 'abraham_lincoln'
        data = {'username': username}
        json_data = json.dumps(data)

        response = self.client_player_a.post(self.profile_url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 202)


    def test_player_creates_new_game(self):
        pass
