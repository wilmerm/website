"""
Esto hace que todas las views de todas las aplicaciones, hereden estas
variables en su contexto para que todas las plantillas dispongan de esto
sin tener que desclararlas en las views.

Es necesario agregar 'base.context_processors.[NAME]' en el setting.py en la
parte de TEMPLATES -- OPTIONS -- context_procesors

"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _
from django.db.utils import OperationalError

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide,
Schedule, BrandRepresented, Question, SampleImage, SampleVideo)

try:
    from store.models import Item, StoreSetting
except (ImportError):
    pass




# Obtiene el site actual.
def get_current_site(request=None):
    try:
        return Site.objects.get_current()
    except (NameError) as e:
        print(e)



class Base:
    """
    Métodos abreviadas para la aplicación 'base'.
    """

    def __str__(self):
        return self.setting().website_name or "base"

    @classmethod
    def social_networks(self, request=None):
        try:
            return SocialNetwork.on_site.all()
        except (OperationalError) as e:
            print(e)
        
    @classmethod
    def setting(self, request=None):
        try:
            return Setting.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def advanced_setting(self, request=None):
        try:
            return AdvancedSetting.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sliders(self, request=None):
        try:
            return Slide.on_site.filter(is_active=True)
        except (OperationalError) as e:
            print(e)

    @classmethod
    def schedule(self, request=None):
        try:
            return Schedule.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def brands(self, request=None):
        try:
            return BrandRepresented.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def questions(self, request=None):
        try:
            return Question.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_images(self, request=None):
        try:
            return SampleImage.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_videos(self, request=None):
        try:
            return SampleVideo.on_site.all()
        except (OperationalError) as e:
            print(e)



class Store:
    """
    Métodos abreviados para la aplicación 'store'.
    """

    def __str__(self):
        return "%s Store" % (Base())

    def __bool__(self):
        try:
            StoreSetting
        except (NameError):
            return False
        return True

    @classmethod
    def items(self, request=None):
        try:
            return Item.on_site.filter(is_active=True)
        except (NameError) as e:
            print(e)

    @classmethod
    def setting(self, request=None):
        try:
            return StoreSetting.on_site.last()
        except (NameError) as e:
            print(e)

    @classmethod
    def featured_items(self, request=None):
        try:
            return Item.on_site.filter(is_active=True, is_featured=True)
        except (NameError) as e:
            print(e)




CONTEXT = {

    # Unolet
    "unolet": {
        "author": "Unolet",
        "site": {
            "url": "https://www.unolet.com",
            "url_clean": "www.unolet.com",
            "name": "Unolet",
        },
    },
    
    "settings": settings, # app.settings.base

    "base": Base,

    "store": Store,

    "get_current_site": get_current_site,

}


def var(request):
    """
    Variables globales.
    """
    return CONTEXT