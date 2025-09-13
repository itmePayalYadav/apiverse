import jwt 
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return token
        if token.startswith("Bearer "):
            token = token[7:]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])
            return (user, token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed("Invalid or expired token")
        