from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player, GameSession

# display Player model on admin index page
admin.site.register(Player, UserAdmin)
admin.site.register(GameSession)
