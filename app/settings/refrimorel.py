from .base import *


NAME = "refrimorel"

SECRET_KEY = ')i-)cyg((ap3*ad6g2#$314z9*b%qo5114c2+zmdtqbo~@|¬s5'

#DEBUG = False

#ALLOWED_HOSTS = [f"www.{NAME}.com", f"{NAME}.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / f'db/{NAME}.sqlite3',
    }
}

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"] = [BASE_DIR / f"templates/{NAME}"]