from django.conf import settings
from suapintegration import default_settings


name = "suapintegration"


def get_setting(key):
    return getattr(settings, key, getattr(default_settings, key))
