from datetime import timedelta
from django.conf import settings

JWT_SECRET = getattr(settings, "JWT_SECRET", settings.SECRET_KEY)
JWT_ALGORITHM = getattr(settings, "JWT_ALGORITHM", "HS256")
JWT_ISSUER = getattr(settings, "JWT_ISSUER", "gms")
JWT_AUDIENCE = getattr(settings, "JWT_AUDIENCE", "gms.api")
JWT_ACCESS_LIFETIME = timedelta(minutes=getattr(settings, "JWT_ACCESS_MINUTES", 30))
JWT_REFRESH_LIFETIME = timedelta(days=getattr(settings, "JWT_REFRESH_DAYS", 7))
