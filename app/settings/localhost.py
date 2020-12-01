from .base import *



SECRET_KEY = ')i-)cyg((ap3*-asg2#$314z9*b%qo56wgc2+zmdtqbo@*i3!$'

DEBUG = True

ALLOWED_HOSTS = ["localhost", "*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = MEDIA_ROOT / "localhost"