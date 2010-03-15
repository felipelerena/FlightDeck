from django.conf import settings

# ------------------------------------------------------------------------
# TODO: make things work if True
JETPACK_NEW_IS_BASE = False

JETPACK_ITEMS_PER_PAGE = getattr(settings, 'JETPACK_ITEMS_PER_PAGE', 10)
