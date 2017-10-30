# Design Questions

Integrate with other django apps? 
Better to use default authentication + extend

Otherwise - I'm subclassing AbstractBaseUser

email required?
log in with email? 
log in with username is django admin default

reason - usernames are not secure (not that emails are either)

oauth2
http://www.tomchristie.com/rest-framework-2-docs/api-guide/authentication#json-web-token-authentication
-library is not maintained

internationalization and language

on_delete argument for association table?

-----------------

# Data
superuser
me@me.com
me
password:
fakefake

make many to many table with game sessions

# chinese characters
in username encoding -- utf-16?

verify username is urlsave -- or change capture group/url displayed for user - or convert to utf8 for url w/urllib
probably doesn't matter if this is for game console - won't see url navigation


---------
# things I needed to do to create a custom user:
set 
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'confirmed']

may need custom user manager

 # outline

 create users
 create game sessions mapped to users

 make sure user can view own settings
 make sure user can change own settings

 make sure user can't view other person's settings profile
 make sure user can't change other person's settings profile
 
 repeat for game data!

---

primary key on user -- should username be changeable? reuseable by other players if player changes name?


# Password
eek! I can use player.password in the shell and get it back plaintext!!!!

