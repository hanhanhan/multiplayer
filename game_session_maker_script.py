from unity_userdata.models import GameSession, GameSession_Player, Player

Player.generate_fake()
player = Player.objects.()
x_position = -5000
y_position = 1000
level = 34
points = 789098 

game_session = GameSession()
player = Player.objects.order_by('?').first()
GameSession_Player(player=player, game=game_session)


