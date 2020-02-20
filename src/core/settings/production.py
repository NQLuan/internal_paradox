from .base import *

# For security and performance reasons, DEBUG is turned off
DEBUG = False

CUSTOM_DOMAIN = env('CUSTOM_DOMAIN')
STATIC_URL = 'http://{0}/{1}/'.format(CUSTOM_DOMAIN, 'static')

# Media S3 config
MEDIA_URL = 'http://{0}/{1}/'.format(CUSTOM_DOMAIN, 'media')
