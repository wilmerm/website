from .base import *



SECRET_KEY = ')i-)cyg((ap3*ad6g2#$314z9*b%qo5114c2+zmdtqbo~@|¬s5'

DEBUG = False

ALLOWED_HOSTS = ["www.refrimorel.com", "refrimorel.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db/refrimorel.sqlite3',
    }
}

MEDIA_ROOT = MEDIA_ROOT / "refrimorel"
