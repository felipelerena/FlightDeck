PROJECT_PATH = '/path/to/projects/FlightDeck'
ALLDIRS = ['%s/flightdeckenv/lib/python2.5/site-packages' % PROJECT_PATH]

import sys
import os
import site

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
for directory in ALLDIRS:
    site.addsitedir(directory)

# add the app's directory to the PYTHONPATH
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append('%s/flightdeckenv/lib/python2.6/site-packages/' % PROJECT_PATH)
sys.path.append('%s/' % PROJECT_PATH)
sys.path.append('%s/flightdeck/' % PROJECT_PATH)

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
	sys.path.remove(item)
	sys.path[:0] = new_sys_path


os.environ['CUDDLEFISH_ROOT'] = '/var/www/FlightDeck/flightdeckenv'
os.environ['PATH'] = os.environ['PATH'] + ':/var/www/FlightDeck/flightdeckenv/bin'

os.environ['DJANGO_SETTINGS_MODULE'] = 'flightdeck.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


