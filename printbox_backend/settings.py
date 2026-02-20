"""
Django settings for printbox_backend project.
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os
import sys
from datetime import timedelta

# -------------------------------------------------------------------------
# PATHS
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-key-change-in-production")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,www.printbox3d.com,printbox3d.com,www.printbox3d.in,printbox3d.in,web-production-d7d11.up.railway.app",
    cast=Csv(),
)

# -------------------------------------------------------------------------
# INSTALLED APPS
# -------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "storages",

    # Local apps
    "api",
]

# -------------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST be first for CORS to work
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "printbox_backend.urls"

# -------------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "printbox_backend.wsgi.application"

# -------------------------------------------------------------------------
# DATABASES (Railway / Local)
# -------------------------------------------------------------------------
is_migration = "migrate" in sys.argv or "makemigrations" in sys.argv

database_url = config("DATABASE_URL", default="")

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    
    # Add connection timeout
    DATABASES["default"]["OPTIONS"] = {
        "connect_timeout": 10,
    }

    if is_migration:
        direct_url = config("DIRECT_DATABASE_URL", default="")
        if direct_url:
            DATABASES["default"] = dj_database_url.parse(direct_url)
        DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------------
# STATIC FILES (served by WhiteNoise on Railway)
# -------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------------
# MEDIA / FILE STORAGE — S3 in production, local in development
# -------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="printbox-media")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="ap-south-1")

if AWS_ACCESS_KEY_ID:
    # --- Production: store all uploaded files in S3 ---
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_S3_FILE_OVERWRITE = False          # never silently overwrite existing files
    AWS_DEFAULT_ACL = "public-read"        # files are publicly readable (no signed URLs needed)
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",   # browser caches images for 1 day
    }
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    MEDIA_ROOT = ""                        # not used when S3 is active
else:
    # --- Development: use local media folder ---
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------------------------------
# CORS CONFIG
# -------------------------------------------------------------------------
# Read allowed origins from environment (comma-separated).
# Falls back to localhost only (safe for CI / dev environments).
_cors_env = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000,https://www.printbox3d.com,https://printbox3d.com,https://www.printbox3d.in,https://printbox3d.in',
)
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in _cors_env.split(',') if origin.strip()]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
]

CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
]

CORS_PREFLIGHT_MAX_AGE = 86400  # 24 h

CSRF_TRUSTED_ORIGINS = [
    "https://web-production-d7d11.up.railway.app",
    "https://www.printbox3d.com",
    "https://printbox3d.com",
    "https://www.printbox3d.in",
    "https://printbox3d.in",
]

# Cookie security
CSRF_COOKIE_SECURE    = True
CSRF_COOKIE_SAMESITE  = 'None'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

# -------------------------------------------------------------------------
# HTTPS / SECURITY HEADERS (Railway runs behind TLS terminating proxy)
# -------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS     = 31536000   # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD     = True
SECURE_CONTENT_TYPE_NO_SNIFF = True
X_FRAME_OPTIONS         = 'DENY'

# -------------------------------------------------------------------------
# DRF CONFIG
# -------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# -------------------------------------------------------------------------
# SIMPLE JWT
# -------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
}

# -------------------------------------------------------------------------
# EMAIL CONFIG (Standard SMTP)
# -------------------------------------------------------------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"  # Prints to console in development
)

# SMTP Configuration (optional - for production)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="PrintBox3D <noreply@printbox3d.com>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# -------------------------------------------------------------------------
# RAZORPAY CONFIG
# -------------------------------------------------------------------------
RAZORPAY_KEY_ID             = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET         = config('RAZORPAY_KEY_SECRET', default='')
RAZORPAY_WEBHOOK_SECRET     = config('RAZORPAY_WEBHOOK_SECRET', default='')

# -------------------------------------------------------------------------
# FRONTEND URL (used for password reset links in emails)
# -------------------------------------------------------------------------
FRONTEND_URL = config('FRONTEND_URL', default='https://www.printbox3d.com')

