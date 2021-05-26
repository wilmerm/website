from .base import *


NAME = "mundofrio"

# SECRET_KEY = ')i-)cyg((ap3*ad6g2#$314z9*b%qo5114c2+zmdtqbo~@|¬s5'

ALLOWED_HOSTS = ["*", f"www.{NAME}.com", f"{NAME}.com"]

MEDIA_ROOT = MEDIA_ROOT / NAME

TEMPLATES[0]["DIRS"].append(BASE_DIR / f"templates/{NAME}")

SITE_ID = 4

UNOLET_APP_DOMAIN = "www.mundofrio.net"