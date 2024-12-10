"""
Django settings for GameHQ project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4^=6s^u9^x)eq!3)xclsm0kn25mk%o578nt-ap54i4$utva--_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',  # Home page app
    'games',  # Games page app
    'about_us',  # About Us page app
    'contact',  # Contact page app
    'core',
    'games_db',
    'register',
    'search',
    'Add_Game',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GameHQ.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Project-level templates directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.login_form_context',
                'core.context_processors.signup_form_context',
                'games_db.context_processors.cart_count', 
                'games.context_processors.genre_context',
                'games.context_processors.star_range_context', 
            ],
        },
    },
]

WSGI_APPLICATION = 'GameHQ.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            "transaction_mode": "IMMEDIATE",
            'timeout': 60,  # Wait 20 seconds before raising "database is locked"
        },
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Add the static directory at the project level
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Media URL and Root configuration
MEDIA_URL = '/media/'  # URL path to access media files in the browser
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory where media files are stored on the server

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'games_db.CustomUser' 
LOGIN_REDIRECT_URL = '/'  # Redirect to home page after login
LOGOUT_REDIRECT_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Ends session on browser close
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session expiry on every request
SESSION_COOKIE_AGE = 3600  # Session expires after 1 hour
SESSION_COOKIE_SECURE = True  # Ensures cookies are sent only over HTTPS
SESSION_COOKIE_HTTPONLY = False  # Makes the session cookie inaccessible via JavaScript

X_FRAME_OPTIONS = 'DENY'

SECURE_SSL_REDIRECT = False  # Redirect all HTTP to HTTPS
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False


CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'",)

# Email settings for Gmail (can be adjusted for other services)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'chris.k.dimopoulos@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-email-password'  # Your Gmail password or app-specific password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER