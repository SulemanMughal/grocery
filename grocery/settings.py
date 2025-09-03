from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

# import apps.authn.schema_extensions


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SQLITE_PATH = config("SQLITE_PATH", "/data/sqlite/db.sqlite3")


INSTALLED_APPS = [

    # ────────────────
    # Built-in apps
    # ────────────────
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    # ────────────────
    # 3rd party apps
    # ────────────────

    # Neo4j
    'django_neomodel' ,

    # API Development
    "rest_framework",

    # CORS 
    "corsheaders",

    # API Documentation
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # ────────────────
    # Local apps
    # ────────────────

    'apps.users',
    'apps.authn',
    'apps.groceries',
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],                 # add custom template dirs here if you have any
        "APP_DIRS": True,          # <-- required so Django loads templates from app packages
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
            ],
        },
    },
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'common.middleware.CorrelationIdMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'grocery.urls'
WSGI_APPLICATION = 'grocery.wsgi.application'


# ──────────────────────────────────────────────────────────────────────────────
# Django DB (not used for domain; keep minimal sqlite to satisfy Django checks)
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
        "NAME": SQLITE_PATH,
    }
}


# ──────────────────────────────────────────────────────────────────────────────
# Neo4j / neomodel (via django_neomodel)
# ──────────────────────────────────────────────────────────────────────────────
NEOMODEL_NEO4J_BOLT_URL = config('NEOMODEL_NEO4J_BOLT_URL')
NEOMODEL_SIGNALS = config('NEOMODEL_SIGNALS', default=True, cast=bool)
NEOMODEL_FORCE_TIMEZONE = config('NEOMODEL_FORCE_TIMEZONE', default=True, cast=bool)
NEOMODEL_MAX_CONNECTION_POOL_SIZE = config('NEOMODEL_MAX_CONNECTION_POOL_SIZE', default=30, cast=int)
NEOMODEL_DATABASE = config("NEOMODEL_DATABASE", default="neo4j")



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

STATIC_ROOT= BASE_DIR / 'static'
STATICFILES_DIRS=[
]


# Media Settings
MEDIA_URL = '/media/'
MEDIA_ROOT= BASE_DIR.parent / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# ──────────────────────────────────────────────────────────────────────────────
# DRF & JWT (SimpleJWT)
# ──────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS" : "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_SCHEMA_CLASS": "apps.schema_auth.GlobalHeaderAuthSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        'apps.authn.authentication.CustomJWTAuthentication',
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "1",
    "ALLOWED_VERSIONS": ("1",),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "1000/day",  # 1000 requests per day
        "anon": "100/day",  # 100 requests per day
    },
    "EXCEPTION_HANDLER": "common.exceptions.drf_exception_handler",
    
}


# JWT config 
JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_ISSUER = "grocery"
JWT_AUDIENCE = "grocery.api"
JWT_ACCESS_MINUTES = int(config("JWT_ACCESS_MINUTES", default="30"))
JWT_REFRESH_DAYS = int(config("JWT_REFRESH_DAYS", default="7"))



# ──────────────────────────────────────────────────────────────────────────────
# API Documentation (drf-spectacular)
# ──────────────────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "Grocery API",
    "DESCRIPTION": "REST API for managing groceries, items, suppliers, and daily income.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1",  # only include your versioned routes
    "COMPONENT_SPLIT_REQUEST": True,
    "POSTPROCESSING_HOOKS": ["drf_spectacular.hooks.postprocess_schema_enums"],
    "SWAGGER_UI_DIST": "SIDECAR",   # use sidecar assets
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'], # change it for production
    
    # Security configuration for JWT Bearer auth
    # "SECURITY": [{"BearerAuth": []}],
    "SECURITY": [{"bearerAuth": []}],

    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Paste your access token **without** the word Bearer here; "
                               "Swagger will add the prefix automatically.",
            }
        }
    },
    
    # Swagger UI settings
    'SWAGGER_UI_SETTINGS': {
        'filter': True,
        'persistAuthorization': True,
        'deepLinking': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        'defaultModelRendering': 'example',
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'operationsSorter': 'alpha',
        'showExtensions': True,
        'showCommonExtensions': True,
        'tagsSorter': 'alpha'
    },
}



# ──────────────────────────────────────────────────────────────────────────────
# CORS / CSRF
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL", default="True", cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())



# ──────────────────────────────────────────────────────────────────────────────
# Logging (structured, concise)
# ──────────────────────────────────────────────────────────────────────────────


# Where to put logs inside the container (overridable via env)
DJANGO_LOG_DIR = Path(config("DJANGO_LOG_DIR", BASE_DIR / "logs"))
DJANGO_LOG_FILE = DJANGO_LOG_DIR / "django.log"

LOG_TO_FILE = config("LOG_TO_FILE", default="1", cast=bool)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(process)d | %(thread)d | %(message)s",
        },
        "simple": {"format": "%(levelname)s | %(name)s | %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        },
        # File handler is optional; directory must exist
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": str(DJANGO_LOG_FILE),   # <-- str, not Path
            "maxBytes": 10 * 1024 * 1024,      # 10 MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"] + (["file"] if LOG_TO_FILE else []),
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"] + (["file"] if LOG_TO_FILE else []),
            "level": "DEBUG",
            "propagate": False,
        },
        "common": {
            "handlers": ["console"] + (["file"] if LOG_TO_FILE else []),
            "level": "DEBUG",
            "propagate": False,
        },
        # your app modules can be listed here too
        "": {  # root logger
            "handlers": ["console"] + (["file"] if LOG_TO_FILE else []),
            "level": "INFO",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Security (tighten in prod)
# ──────────────────────────────────────────────────────────────────────────────
# SECURE_PROXY_SSL_HEADER = config("HTTP_X_FORWARDED_PROTO", default="https")
# SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
# CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
# SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default="False", cast=bool)