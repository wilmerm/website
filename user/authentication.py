"""
Autenticación de usuario personalizada.

"""

from django.conf import settings
from django.utils.translation import gettext

try:
    from google.oauth2 import id_token
    from google.auth.transport import requests
except (ImportError) as e:
    print(e)

from .models import User




class AuthByEmailBackend:
    """
    Backend personalizado de authenticaciónd de 
    usuario via email en el sitio actual.

    """
    def authenticate(self, request, username=None, password=None):

        try:
            # En nuestro modelo User hemos definido un manejador 'on_site' que
            # que sería igual a:
            # User.objects.filter(site=Site.objects.get_current())
            # También determinamos que el email será 
            # único solo para el site en actual.
            user = User.on_site.get(email=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.on_site.get(pk=user_id)
        except (User.DoesNotExist):
            return None






def google_verify_token(request):
    """

    https://developers.google.com/identity/sign-in/web/backend-auth
    """
    # (Receive token by HTTPS POST)
    token = request.POST.get("idtoken")
    CLIENT_ID = settings.GOOGLE_API_CLIENT_ID

    print(f"google_verify_token(request): '{token}'")
    fname = "user.authentication.google_verify_token(request)."

    if not token:
        raise ValueError(f"{fname}. Falta el parámetro 'idtoken' pasado por "
        "request.POST.")

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except (ValueError) as e:
        raise ValueError(f"{fname}. No fue posible la validación del usuario. {e}.")
    
    return {"idinfo": idinfo, "userid": userid}