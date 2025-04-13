from django.http.request import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    """
        Ici on fait juste une surcharge de la fonction authenticate de JWTAuthentication pour recuperer les tokens( access token) a partir du access cookie si present(pour des raisons de securité_), 
        A defaut de la presence du access token a partir du headers de la requete  
    """
    
    def authenticate(self, request: HttpRequest):
        try:
            header = self.get_header(request)
            
            if header is None:
                #on recuperer le token à partir du  cookie access
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)
                
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None
