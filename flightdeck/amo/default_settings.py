from django.conf import settings

# ------------------------------------------------------------------------
AMO_LIMITED_ACCESS = getattr(settings, 'AMO_LIMITED_ACCESS', False)
