from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.config import settings

# Initialize OAuth
config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID or "",
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET or "",
    "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID or "",
    "FACEBOOK_APP_SECRET": settings.FACEBOOK_APP_SECRET or "",
})

oauth = OAuth(config)

# Register Google OAuth
if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

# Register Facebook OAuth
if settings.FACEBOOK_APP_ID and settings.FACEBOOK_APP_SECRET:
    oauth.register(
        name='facebook',
        client_id=settings.FACEBOOK_APP_ID,
        client_secret=settings.FACEBOOK_APP_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth',
        api_base_url='https://graph.facebook.com/',
        client_kwargs={
            'scope': 'email public_profile'
        }
    )
