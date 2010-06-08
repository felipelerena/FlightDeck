from django.conf import settings

PACKAGES_PER_PAGE =  getattr(settings, 'PACKAGES_PER_PAGE', 10)
MINIMUM_PACKAGE_ID = getattr(settings, 'MINIMUM_PACKAGE_ID', 1000000)
INITIAL_VERSION_NAME = getattr(settings, 'INITIAL_VERSION_NAME', 'initial')
UPLOAD_DIR = getattr(settings, 'UPLOAD_DIR', '%s/upload' % settings.FRAMEWORK_PATH)
DEFAULT_LIB_DIR = getattr(settings, 'JETPACK_LIB_DIR', 'lib')
DEFAULT_DATA_DIR = getattr(settings, 'JETPACK_DATA_DIR', 'data')
PACKAGE_PLURAL_NAMES = {
	'l': 'libraries',
	'a': 'addons'
}
PACKAGE_SINGULAR_NAMES = {
	'l': 'library',
	'a': 'addon'
}
HOMEPAGE_PACKAGES_NUMBER = getattr(settings, 'HOMEPAGE_PACKAGES_NUMBER', 3)
SDKDIR_PREFIX = '/tmp/SDK'
LIBRARY_AUTOCOMPLETE_LIMIT = getattr(settings, 
								'JETPACKLIBRARY_AUTOCOMPLETE_LIMIT', 20)
KEYDIR = 'keydir'

# ------------------------------------------------------------------------
JETPACK_NEW_IS_BASE = False # it shouldn't be changed
JETPACK_ITEMS_PER_PAGE = getattr(settings, 'JETPACK_ITEMS_PER_PAGE', 10)

# TODO: check if thatr's really needed
# ------------------------------------------------------------------------
VIRTUAL_ENV = settings.VIRTUAL_ENV
VIRTUAL_SITE_PACKAGES = settings.VIRTUAL_SITE_PACKAGES
FRAMEWORK_PATH = settings.FRAMEWORK_PATH
DEBUG = settings.DEBUG
HOMEPAGE_ITEMS_LIMIT = settings.HOMEPAGE_ITEMS_LIMIT 
