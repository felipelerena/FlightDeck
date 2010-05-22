from django.conf import settings

# ------------------------------------------------------------------------
JETPACK_NEW_IS_BASE = False # it shouldn't be changed
JETPACK_ITEMS_PER_PAGE = getattr(settings, 'JETPACK_ITEMS_PER_PAGE', 10)
MINIMUM_PACKAGE_ID = getattr(settings, 'MINIMUM_PACKAGE_ID', 1000000)
INITIAL_VERSION_NAME = getattr(settings, 'INITIAL_VERSION_NAME', 'initial')
UPLOAD_DIR = getattr(settings, 'UPLOAD_DIR', '%s/upload' % settings.FRAMEWORK_PATH)
DEFAULT_LIB_DIR = getattr(settings, 'JETPACK_LIB_DIR', 'lib')
DEFAULT_STATIC_DIR = getattr(settings, 'JETPACK_STATIC_DIR', 'lib')

# TODO: check if thatr's really needed
VIRTUAL_ENV = settings.VIRTUAL_ENV
VIRTUAL_SITE_PACKAGES = settings.VIRTUAL_SITE_PACKAGES
FRAMEWORK_PATH = settings.FRAMEWORK_PATH
DEBUG = settings.DEBUG
HOMEPAGE_ITEMS_LIMIT = settings.HOMEPAGE_ITEMS_LIMIT 
