from .base import *


NAME = "refrinverter"

SECRET_KEY = ')i-)cyg((ap3*ad6(2#$001z9*b%qo$/-4c2+zm4tqbo~@|¬sz'

DEBUG = False

ALLOWED_HOSTS = [f"www.{NAME}.com", f"{NAME}.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wilmermartinez$websites',
        'USER': 'wilmermartinez',
        'PASSWORD': 'HolaMundo',
        'HOST': 'wilmermartinez.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'TEST': {
            'NAME': 'wilmermartinez$test',
        },
    },
}

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"].append(BASE_DIR / f"templates/{NAME}")

SITE_ID = 3