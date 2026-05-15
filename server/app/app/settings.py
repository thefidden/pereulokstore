"""
Настройки Django проекта интернет-магазина.

Основные компоненты:
- Django REST Framework для API
- PostgreSQL с поддержкой полнотекстового поиска (trigram)
- Аутентификация через Telegram
- Интеграция с платежной системой Альфа-Банк
- Профилирование запросов через Django Silk
- Мониторинг ошибок через Sentry
- CORS для фронтенд-приложений
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import sentry_sdk

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['pereulokstore.ru', 'www.pereulokstore.ru', 'localhost', '127.0.0.1', '26.189.158.154']

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django_filters',
    'django.contrib.admin',
    'app.auth_config.BigAuthConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'api',
    'telegram_bot',
    'rest_framework',
    'corsheaders',
    'silk',
    'import_export'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.HTMLFormRenderer'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'app.asgi.application'
WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT')
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_AGE = 5

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://192.168.0.100:5173',
                        'http://26.105.14.122:5173']
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://192.168.0.100:5173',
                        'http://26.105.14.122:5173', 'https://pereulokstore.ru', 'https://www.pereulokstore.ru']

SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True
CSFR_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REPORTS_URL = 'reports/'
REPORTS_ROOT = os.path.join(BASE_DIR, 'reports')

CYRILLIC_FONT_NAME = 'helvetica_cyr_boldoblique'
CYRILLIC_FONT_PATH = os.path.join(STATIC_ROOT, 'fonts', 'helvetica_cyr_boldoblique.ttf')

LANGUAGE_CODE = 'ru'

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALFA_BANK_TOKEN = os.getenv('ALFA_BANK_TOKEN')
ALFA_BANK_USERNAME = os.getenv('ALFA_BANK_USERNAME')
ALFA_BANK_PASSWORD = os.getenv('ALFA_BANK_PASSWORD')

# =============================================================================
# Sentry Configuration — Мониторинг ошибок
# =============================================================================

import sentry_sdk

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn = SENTRY_DSN,
        traces_sample_rate = 0.1,  # 10% запросов для performance monitoring
        profiles_sample_rate = 0.1,  # 10% профилирования
        environment = 'production' if not DEBUG else 'development',
        # Отправлять информацию о релизе
        release = os.environ.get('RELEASE_VERSION', 'unknown'),
    )

# =============================================================================
# Django Silk Configuration — Профилирование запросов
# =============================================================================

# Silk доступен только в DEBUG режиме и не в тестах
SILKY_PYTHON_PROFILER = False  # Отключено из-за конфликта с Daphne (ASGI)
SILKY_PYTHON_PROFILER_BINARY = False
SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'profiles')

# Авторизация для доступа к Silk (только для staff пользователей)
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True

# Максимальное количество запросов в БД Silk
SILKY_MAX_REQUEST_BODY_SIZE = 1024 * 1024  # 1MB
SILKY_MAX_RESPONSE_BODY_SIZE = 1024 * 1024  # 1MB

# Автоматическая очистка старых записей (опционально)
SILKY_MAX_RECORDED_REQUESTS = 10000
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10

sentry_sdk.init(
    dsn = os.getenv('SENTRY_DSN'),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii = True,
)
