"""
Esto hace que todas las views de todas las aplicaciones, hereden estas
variables en su contexto para que todas las plantillas dispongan de esto
sin tener que desclararlas en las views.

Es necesario agregar 'base.context_processors.[NAME]' en el setting.py en la
parte de TEMPLATES -- OPTIONS -- context_procesors

"""

from django.conf import settings
from django.utils.translation import gettext as _

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide,
Schedule, Brand, Question)

try:
    from store.models import Item
except (ImportError):
    pass


class Base:

    @classmethod
    def social_networks(self, request=None):
        return SocialNetwork.objects.all()

    @classmethod
    def setting(self, request=None):
        return Setting.objects.last()

    @classmethod
    def advanced_setting(self, request=None):
        return AdvancedSetting.objects.last()

    @classmethod
    def sliders(self, request=None):
        return Slide.objects.filter(is_active=True)

    @classmethod
    def schedule(self, request=None):
        return Schedule.objects.last()

    @classmethod
    def brands(self, request=None):
        return Brand.objects.all()

    @classmethod
    def questions(self, request=None):
        return Question.objects.all()



class Store:

    @classmethod
    def items(self, request=None):
        try:
            return Item.objects.filter(is_active=True)
        except (NameError) as e:
            print(e)

    @classmethod
    def featured_items(self, request=None):
        try:
            return Item.objects.filter(is_active=True, is_featured=True)
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

}


def var(request):
    """
    Variables globales.
    """
    return CONTEXT