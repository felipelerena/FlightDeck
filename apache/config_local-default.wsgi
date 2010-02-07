import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 

sys.path.append('/path/to/projects/FlightDeck/flightdeckenv/lib/python2.6/site-packages/')
sys.path.append('/path/to/projects/FlightDeck/')
sys.path.append('/path/to/projects/FlightDeck/flightdeck/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'flightdeck.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


