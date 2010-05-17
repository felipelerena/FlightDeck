from django.conf import settings

# ------------------------------------------------------------------------
JETPACK_NEW_IS_BASE = False # it shouldn't be changed
JETPACK_ITEMS_PER_PAGE = getattr(settings, 'JETPACK_ITEMS_PER_PAGE', 10)
MINIMUM_PACKAGE_ID = getattr(settings, 'MINIMUM_PACKAGE_ID', 1000000)
INITIAL_VERSION_NAME = getattr(settings, 'INITIAL_VERSION_NAME', 'initial')

# TODO: check if thatr's really needed
VIRTUAL_ENV = settings.VIRTUAL_ENV
VIRTUAL_SITE_PACKAGES = settings.VIRTUAL_SITE_PACKAGES
FRAMEWORK_PATH = settings.FRAMEWORK_PATH
DEBUG = settings.DEBUG
HOMEPAGE_ITEMS_LIMIT = settings.HOMEPAGE_ITEMS_LIMIT 
