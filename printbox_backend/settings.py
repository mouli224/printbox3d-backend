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
    default="localhost,127.0.0.1,www.printbox3d.com,printbox3d.com,web-production-d7d11.up.railway.app",
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
# STATIC & MEDIA FILES
# -------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------------
# CORS CONFIG (Correct + Razorpay safe)
# -------------------------------------------------------------------------
# Allow all origins for now (can restrict later)
CORS_ALLOW_ALL_ORIGINS = True

# Explicit allowed origins (backup if ALLOW_ALL doesn't work)
CORS_ALLOWED_ORIGINS = [
    "https://www.printbox3d.com",
    "https://printbox3d.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Allow all methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "cache-control",
]

CORS_EXPOSE_HEADERS = [
    "content-type",
    "x-csrftoken",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
]

CORS_PREFLIGHT_MAX_AGE = 86400  # Cache preflight for 24 hours

CSRF_TRUSTED_ORIGINS = [
    "https://web-production-d7d11.up.railway.app",
    "https://www.printbox3d.com",
    "https://printbox3d.com",
    "https://www.printbox3d.in",
    "https://printbox3d.in",
]


# Exempt payment verification from CSRF (uses Razorpay signature instead)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

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
# EMAIL CONFIG (Mailgun SMTP)
# -------------------------------------------------------------------------
EMAIL_HOST = config("EMAIL_HOST", default="smtp.mailgun.org")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="printbox3d@sandbox2385eaf1e38341cbbd70502b7e54ce7e.mailgun.org")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # Set this in Railway Variables
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="info@printbox3d.com")
EMAIL_TIMEOUT = 30  # 30 second timeout for email operations

# Custom relaxed SSL backend for better compatibility
import ssl
import smtplib
import socket
from django.core.mail.backends.smtp import EmailBackend as BaseEmailBackend

class CustomEmailBackend(BaseEmailBackend):
    def open(self):
        if self.connection:
            return False
        
        try:
            # Force IPv4 to avoid IPv6 issues
            old_getaddrinfo = socket.getaddrinfo
            def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
                return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
            socket.getaddrinfo = getaddrinfo_ipv4_only
            
            try:
                # Use SMTP_SSL for port 465, regular SMTP for port 587
                if self.use_ssl:
                    # SSL connection (port 465)
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    self.connection = smtplib.SMTP_SSL(
                        self.host, 
                        self.port, 
                        timeout=30,
                        context=context
                    )
                else:
                    # TLS connection (port 587)
                    self.connection = smtplib.SMTP(
                        self.host, 
                        self.port, 
                        timeout=30
                    )
                    if self.use_tls:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        self.connection.starttls(context=context)
                
                # Login
                if self.username and self.password:
                    self.connection.login(self.username, self.password)
                
                return True
            finally:
                # Restore original getaddrinfo
                socket.getaddrinfo = old_getaddrinfo
                
        except Exception as e:
            import logging
            logging.error(f"SMTP connection failed: {e}", exc_info=True)
            if not self.fail_silently:
                raise
            return False

EMAIL_BACKEND = "printbox_backend.settings.CustomEmailBackend"

# -------------------------------------------------------------------------
# RAZORPAY CONFIG
# -------------------------------------------------------------------------
RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID", default="")
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET", default="")
