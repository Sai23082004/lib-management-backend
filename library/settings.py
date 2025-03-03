"""
Django settings for library project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x0m=mp$##cci54-nywqi@+uhiiue755kf!)^5&@88l+qb=mx65'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',  # Allow local development
    'localhost',   # Allow local development
    'lib-management-backend-hu2z.onrender.com', 
     'https://selflibrary.netlify.app/', # Add your Render domain
]


# Application definition

INSTALLED_APPS = [
    'project',
    'users',
    'rest_framework',
    'corsheaders',
    "rest_framework_simplejwt",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ CORS middleware for cross-origin requests
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ REQUIRED for authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ REQUIRED for messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5500",  # Add your frontend domain (if React/Vite)
    "http://localhost:3000", 
    "https://lib-management-backend-hu2z.onrender.com" ,
     "https://selflibrary.netlify.app/", # Backend URL if necessary
]

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


# Gmail SMTP server settings
EMAIL_HOST = 'smtp.gmail.com'  # The SMTP server for Gmail
EMAIL_PORT = 587  # The SMTP port for Gmail
EMAIL_USE_TLS = True  # Use TLS (recommended by Gmail)
EMAIL_HOST_USER = 'saiteja084084@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default email address for sending emails


ROOT_URLCONF = 'library.urls'

CORS_ALLOW_CREDENTIALS = True  # ✅ Allow cookies and authentication headers

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",  # ✅ Your frontend
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:5173",  # Vite frontend
    "https://selflibrary.netlify.app"  # Your deployed frontend
]

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

CORS_ALLOW_HEADERS = [
    "Authorization",
    "content-type",
    "X-CSRFToken",
    "x-requested-with"
]

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

WSGI_APPLICATION = 'library.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_ymzr',
        'USER': 'root',
        'PASSWORD': 'vSZMh595HRObr20Rkqa1xazOl9igq4OY',
        'HOST': 'dpg-cv2j4qdds78s73eddj60-a',  # Use '127.0.0.1' if needed
        'PORT': '5432',  # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
