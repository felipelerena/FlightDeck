import os.path
import re

FRAMEWORK_PATH = os.path.dirname(os.path.dirname(__file__)) +'/'

ADMINS = (
   # ('Your Name', 'your_email@domain.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Change 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(FRAMEWORK_PATH,'dev.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
MEDIA_ROOT = ''
MEDIA_URL = ''
SECRET_KEY = '_878&mu1t!-d*u^*@l$afwe$p4r(=*$kyyjy37ibf9t8li5#lv'

DEBUG = False

INTERNAL_IPS = ('127.0.0.1',)

MEDIA_ROOT =  os.path.join(FRAMEWORK_PATH, 'flightdeck/media/')
ADMIN_MEDIA_ROOT = os.path.join(FRAMEWORK_PATH, 'flightdeck/adminmedia/')
#MEDIA_URL = '/sitemedia/'
#MEDIA_SERVER = ''
#ADMIN_MEDIA_PREFIX = ''.join([MEDIA_SERVER,'/adminmedia/'])

# dot command path (for the graphviz app)
#GRAPHVIZ_DOT_CMD = '/usr/bin/dot'

ACTIVATE_THIS = '/path/to/flightdeckenv/bin/activate_this.py'
VIRTUAL_ENV = '/path/to/flightdeckenv'
VIRTUAL_SITE_PACKAGES = '/path/to/flightdeckenv/lib/python-2.6/site-packages'
