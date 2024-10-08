import os
import pathlib

import dotenv


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'so-secret')

DEBUG = os.getenv('debug', 't').lower() in ('y', 'yes', '1', 't', 'true')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'artists.apps.ArtistsConfig',
    'download.apps.DownloadConfig',
    'feedback.apps.FeedbackConfig',
    'galleries.apps.GalleriesConfig',
    'homepage.apps.HomepageConfig',
    'paintings.apps.PaintingsConfig',
    'users.apps.UsersConfig',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'sorl.thumbnail',
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

ROOT_URLCONF = 'artina.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',)

WSGI_APPLICATION = 'artina.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
STATIC_ROOT = BASE_DIR / 'static'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = 'homepage:home'
LOGOUT_REDIRECT_URL = 'homepage:home'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

APP_MAIL = os.getenv('APP_MAIL', 'example@gmail.com')
SMTP_MAIL = os.getenv('SMTP_MAIL', 'smtp.gmail.com')
SMTP_KEY = os.getenv('SMTP_KEY', '1234567890')

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
