"""
Archivo de configuración para la versión de desarrollo.

"""

import warnings
from .base import *


NAME = "localhost"

SECRET_KEY = ')i-)cyg((ap3*-asg2#$314z9*b%qo56wgc2+zmdtqbo@*i3!$'

DEBUG = True

ALLOWED_HOSTS = [NAME, "*", "127.0.0.2"]

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
     }
}

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"].append(BASE_DIR / f"templates/mundofrio")

SITE_ID = 1

UNOLET_APP_DOMAIN = "127.0.0.2"
