from .base import *


NAME = "localhost"

SECRET_KEY = ')i-)cyg((ap3*-asg2#$314z9*b%qo56wgc2+zmdtqbo@*i3!$'

DEBUG = True

ALLOWED_HOSTS = [NAME, "*"]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / f'db/{NAME}.sqlite3',
#     }
# }

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"].append(BASE_DIR / f"templates/refrinverter")

SITE_ID = 1