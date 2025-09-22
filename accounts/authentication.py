import jwt 
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return None
        
        if not auth_header.startswith("Bearer "):
            raise exception.AuthenticationFailed("Invalid Authorization header format")

        token = auth_header.split("Bearer ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("id")
            if not user_id:
                raise exceptions.AuthenticationFailed("Invalid token payload")
            user = User.objects.get(id=user_id)
            return (user, token)
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        