from os.path import join

from . import env, BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')
API_HOST = env('API_HOST')
API_PORT = env('API_PORT')
API_BASE = "{0}:{1}".format(API_HOST, API_PORT)
if API_PORT == "80":
    API_BASE = "{0}".format(API_HOST)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[API_BASE, 'api'])

# Application definition
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'rest_framework',
    'corsheaders',
    'django_crontab',
    'sendgrid',
)
LOCAL_APPS = (
    'api',
    'api_base',
    'api_user',
    'api_admin',
    'api_team',
    'api_workday',
    'api_company'
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "api_user.User"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Config django-cors lib
CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', default=False)
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[
    'http://127.0.0.1:8001',
    'http://localhost:8001',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
])
CORS_ORIGIN_REGEX_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Config Django Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomPagination',
    'PAGE_SIZE': 5,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


def db_config(prefix='', test=None):
    if test is None:
        test = {}
    return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': prefix + env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'TEST': test,
        # <fix error Too many connections mysql>
        'OPTIONS': {
            'init_command': 'SET GLOBAL max_connections = 100000',
            'charset': 'utf8mb4'
        }
    }


# Backup Database
REPLICATION_DB_ALIAS = 'replication'
REPLICATION_PREFIX = env('REPLICATION_DB_PREFIX', default='')

DATABASES = {
    'default': db_config(),
    'test': db_config('', {'MIRROR': 'default'}),
    REPLICATION_DB_ALIAS: db_config(REPLICATION_PREFIX)
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
# MEDIA related settings
MEDIA_ROOT = join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# TODO-hoangnguyen Fix later
MEDIA_IMAGE = f'http://{API_HOST}:{API_PORT}'

# EMAIL related settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env("EMAIL_HOST", default='smtp.sendgrid.net')
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default='Management Admin <management-admin@paradox.ai>')
DEFAULT_EMAIL_ADMIN = env("DEFAULT_EMAIL_ADMIN", default='admin@paradox.ai')


CALENDAR_ID = env('CALENDAR_ID')

CRONJOBS = [
    ('0 9 * * 1-5', 'api_base.services.cronjobs.leave_notify'),
    ('45 9 * * 1-5', 'api_base.services.cronjobs.lunch_notify'),
    ('0 6 1 * *', 'api_base.services.cronjobs.lunch_creation')
]

LEAVE_NOTIFICATION_SLACK_API = env('LEAVE_NOTIFICATION_SLACK_API', default='https://hooks.slack.com/services/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')
LUNCH_NOTIFICATION_SLACK_API = env('LUNCH_NOTIFICATION_SLACK_API', default='https://hooks.slack.com/services/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')
