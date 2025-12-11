"""
Django settings for printbox_backend project.
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,www.printbox3d.com,printbox3d.com,www.printbox3d.in,printbox3d.in', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'printbox_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'printbox_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Check if we're running migrations
import sys
is_migration = 'migrate' in sys.argv or 'makemigrations' in sys.argv

# Get database URL from environment
database_url = config('DATABASE_URL', default='')

# Only use PostgreSQL if DATABASE_URL is provided and not empty
if database_url and database_url.strip():
    # Parse the database URL and remove unsupported parameters like ?pgbouncer=true
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    
    # For migrations, use direct connection if available (bypasses PgBouncer)
    if is_migration:
        direct_url = config('DIRECT_DATABASE_URL', default='')
        if direct_url and direct_url.strip():
            DATABASES['default'] = dj_database_url.parse(
                direct_url,
                conn_max_age=0,
                conn_health_checks=False,
            )
        DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True
else:
    # Local development with SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS Settings - TEMPORARY: Allow all origins for testing
# TODO: Restrict this after confirming payment works
CORS_ALLOW_ALL_ORIGINS = True  # TEMPORARY FIX

# Keep these for when we disable CORS_ALLOW_ALL_ORIGINS
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,https://printbox3d.com,https://www.printbox3d.com,https://printbox3d.in,https://www.printbox3d.in',
    cast=Csv()
)

# Additional CORS settings for proper header handling
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
]

CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# CSRF Trusted Origins (for admin panel and forms)
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://web-production-d7d11.up.railway.app,https://printbox3d.com,https://www.printbox3d.com',
    cast=Csv()
)

# Allow credentials
CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours


# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
}

# Email Settings (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@printbox3d.com')

# SSL settings for email
import ssl
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
# Disable SSL certificate verification (for development/Hostinger)
EMAIL_USE_SSL_CERT_VERIFICATION = False

# Create custom SSL context that doesn't verify certificates
import smtplib
from django.core.mail.backends.smtp import EmailBackend as DefaultEmailBackend

class CustomEmailBackend(DefaultEmailBackend):
    def open(self):
        if self.connection:
            return False
        
        connection_params = {'timeout': self.timeout} if self.timeout is not None else {}
        try:
            self.connection = smtplib.SMTP(self.host, self.port, **connection_params)
            
            if self.use_tls:
                # Create SSL context that doesn't verify certificates
                import ssl
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.starttls(context=context)
            
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise

# Use custom backend
EMAIL_BACKEND = 'printbox_backend.settings.CustomEmailBackend'

# Razorpay Configuration
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')
