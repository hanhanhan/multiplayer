from unity_userdata.models import GameSession, Player_GameSession, Player
from unity_userdata.serializers import GameSessionSerializer, PlayerGameSessionSerializer, PlayerGameSessionSerializer

Player.generate_fake()
player = Player.objects.()
x_position = -5000
y_position = 1000
level = 34
points = 789098 

game_session = GameSession()
player = Player.objects.order_by('?').first()
GameSession_Player(player=player, game=game_session)



http POST http://127.0.0.1:8000/ username=exad password=fake
http POST http://127.0.0.1:8000/ Authorization:'Token bc47610da7f6ee27b059d72b5f2d75d9ea7a7ec4'
# For clients to authenticate, the token key should be included in the Authorization HTTP header. 
# The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example:
nullacum
http http://127.0.0.1:8000/profile Authorization:'Token bc47610da7f6ee27b059d72b5f2d75d9ea7a7ec4'
http http://127.0.0.1:8000/profile 'Authorization: Token bc47610da7f6ee27b059d72b5f2d75d9ea7a7ec4'

exad
http http://127.0.0.1:8000/profile Authorization:'Token bfb0b005602989d5a0c1cd5a4392a0229467465e'
http POST -a exad:fake http://127.0.0.1:8000/profile 

import requests
url = 'http://127.0.0.1:8000/profile'
headers = {'Authorization': 'Token bfb0b005602989d5a0c1cd5a4392a0229467465e'}
response = requests.get(url, headers=headers)