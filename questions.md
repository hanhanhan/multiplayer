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

-----------------

# Data
superuser
me@me.com
me
password:
orbitall


---------
# things I needed to do to create a custom user:
set 
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'confirmed']

may need custom user manager


