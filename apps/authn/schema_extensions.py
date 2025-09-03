# e.g. apps/authn/schema_extensions.py
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CustomJWTAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.authn.authentication.CustomJWTAuthentication'  # dotted path
    name = 'bearerAuth'             # the name that will appear in securitySchemes
    match_subclasses = True

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Paste the raw access token; Swagger will add 'Bearer '.",
        }
