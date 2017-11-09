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
        
        self.game_session = GameSession.objects.create()
        self.player_gamesession = Player_GameSession.objects.create(
            game_session=self.game_session, 
            player=self.player_alpha,
            )


        self.player_gamesession = Player_GameSession.objects.create(
            game_session=self.game_session, 
            player=self.player_beta, 
            )

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
         
    
    # Profile related view tests
    
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
        
        print("Error logging from test prints to console:")
        response = client.post(path=url, data=incomplete_json_data, content_type='application/json')
        print("Log complete. \n")
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


    # GameSession related view tests 

    def test_player_can_GET_all_sessions_available(self):
        for i in range(10):
            GameSession.objects.create()

        url = reverse('game_sessions')
        
        response = self.client_player_a.get(url)
        game_session_id = str(self.game_session.game_session_id)
        self.assertContains(response, game_session_id)


    def test_player_POST_can_create_new_game_session(self):
        url = reverse('game_sessions')
        
        response = self.client_player_a.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertIn('x_position', response.data)
        self.assertContains(response, text='x_position', status_code=201)


    # Player_GameSession related view tests

    def test_player_GET_all_own_game_sessions(self):
        url = reverse('player_all_game_sessions')
        
        response = self.client_player_a.get(url)
        self.assertEqual(response.status_code, 200)

        game_sessions = GameSession.objects.all().filter(player=self.player_alpha)
        for session in game_sessions:
            session_id = str(session.game_session_id)
            self.assertContains(response, text=session_id)

        unused_session = GameSession.objects.create()
        unused_session_id = str(unused_session.game_session_id)
        self.assertNotContains(response, text=unused_session_id)


    def test_player_GET_sees_game_session_data(self):
        url = reverse('player_game_session')
        game_session = str(self.game_session.game_session_id)
        data = {'game_session': game_session}
        json_data = json.dumps(data)
        
        response = self.client_player_a.post(url, json_data, content_type='application/json')
        self.assertContains(response, text=game_session)
        # NOTE: Add check that player_beta is returned -- player data for all players needed
        

    def test_player_PUT_updates_game_session_data(self):
        url = reverse('player_game_session')

        keys = ['x_position', 'y_position', 'points']
        values = [101, 501, 12001]
        data = dict(zip(keys, values))
        data['game_session'] = str(self.game_session.game_session_id)
        json_data = json.dumps(data)

        response = self.client_player_a.put(url, json_data, content_type='application/json')
        self.assertContains(response, text='"x_position":101,"y_position":501,"points":12001', status_code=202)


    def test_player_DELETE_removes_player_from_game_session(self):
        url = reverse('player_game_session')
        session_id = str(self.game_session.game_session_id)
        data = {'game_session': session_id}
        json_data = json.dumps(data)
        

        response = self.client_player_a.delete(url, json_data, content_type='application/json')
        
        removed_session = Player_GameSession.objects.all().filter(game_session=session_id, player=self.player_alpha).first()
        self.assertEqual(removed_session, None)
