from django.conf import settings

# ------------------------------------------------------------------------
JETPACK_SLUG_LENGTH = getattr(settings, 'JETPACK_SLUG_LENGTH', 10)

# TODO: make things work if True
JETPACK_NEW_IS_BASE = False
