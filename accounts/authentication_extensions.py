from drf_spectacular.extensions import OpenApiAuthenticationExtension

class JWTAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.authentication.JWTAuthentication'
    name = 'JWTAuth'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }