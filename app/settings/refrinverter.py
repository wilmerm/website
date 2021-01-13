from .base_production import *


NAME = "refrinverter"

#SECRET_KEY = ')i-)cyg((ap3*ad6(2#$001z9*b%qo$/-4c2+zm4tqbo~@|¬sz'

DEBUG = False

ALLOWED_HOSTS = [f"www.{NAME}.com", f"{NAME}.com"]

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"].append(BASE_DIR / f"templates/{NAME}")

SITE_ID = 3

UNOLET_APP_DOMAIN = "refrinverter.unolet.com"