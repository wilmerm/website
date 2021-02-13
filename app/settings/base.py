"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')i-)cyg((bc$lk10vg#$314z9*b%qo56wgc2+zmdtqbo@*i3!$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # Proyecto.
    'user',
    'base',
    'administration',
    'store',

    # Externas.
    'bootstrap4',
    'easy_thumbnails',
    'colorfield',
    'tinymce', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'base.middleware.BaseMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processors.var', # Proyecto.
            ],
            'builtins': [
                'base.templatetags.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



AUTHENTICATION_BACKENDS = [
    'user.authentication.AuthByEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]


LOGIN_REDIRECT_URL = "/accounts/profile/"
#LOGOUT_REDIRECT_URL = "/"

# https://developers.google.com/identity/sign-in/web/backend-auth
# Usado para el inicio o registro de sessión a través de Google Api,
# en el módulo user.authentication
GOOGLE_API_CLIENT_ID = "632095761113-vl3obm2vtre59mihchjoa7nt2mkpopl5.apps.googleusercontent.com"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ","
DECIMAL_SEPARATOR = "."




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "base/static",
    BASE_DIR / "store/static",
    '/var/www/static/',
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# CARGA DE ARCHIVOS
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640 # 15 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20480 # 20 KB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 # 2.5 MB



SITE_ID = 1

AUTH_USER_MODEL = "user.User"


EMAIL_HOST = None # 'smtp.googlemail.com'
EMAIL_PORT = None # 587
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_USE_TLS = True

# Para conectar este sitio con la app Unolet del cliente.
UNOLET_APP_DOMAIN = "demo.unolet.com"


# Aplicación 'easy_thumbnails'
THUMBNAIL_ALIASES = {
    '': {
        'icon': {'size': (32, 32), 'crop': "smart"},
        '64': {'size': (64, 64), 'crop': False},
        '64crop': {'size': (64, 64), 'crop': True},
        '64crop-upscale': {'size': (64, 64), 'crop': True, "upscale": True},

        '128': {'size': (128, 128), 'crop': False},
        '128crop': {'size': (128, 128), 'crop': True},
        '128crop-upscale': {'size': (128, 128), 'crop': True, "upscale": True},
        
        '256': {'size': (256, 256), 'crop': False},
        '256crop': {'size': (256, 256), 'crop': "smart"},
        '256crop-upscale': {'size': (256, 256), 'crop': "smart", "upscale": True},
        
        '512': {'size': (512, 512), 'crop': False},
        '512crop': {'size': (512, 512), 'crop': "smart"},
        '512crop-upscale': {'size': (512, 512), 'crop': "smart", "upscale": True},
        
        '768': {'size': (768, 768), 'crop': False},
        '768crop': {'size': (768, 768), 'crop': "smart"},
        '768crop-upscale': {'size': (768, 768), 'crop': "smart", "upscale": True},
        
        '1024': {'size': (1024, 1024), 'crop': False},
        '1024crop': {'size': (1024, 1024), 'crop': "smart"},
        '1024crop-upscale': {'size': (1024, 1024), 'crop': "smart", "upscale": True},
        '1024x768crop': {'size': (1024, 768), 'crop': "smart"},
    },
}


