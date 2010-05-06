import os
from django.conf import settings


SDKPACKAGESDIR = os.path.join(settings.VIRTUAL_ENV,'src/jetpack-sdk/packages')
# ------------------------------------------------------------------------
VIRTUAL_ENV = settings.VIRTUAL_ENV
VIRTUAL_SITE_PACKAGES = settings.VIRTUAL_SITE_PACKAGES
FRAMEWORK_PATH = settings.FRAMEWORK_PATH
DEBUG = settings.DEBUG
