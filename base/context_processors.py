"""
Esto hace que todas las views de todas las aplicaciones, hereden estas
variables en su contexto para que todas las plantillas dispongan de esto
sin tener que desclararlas en las views.

Es necesario agregar 'base.context_processors.[NAME]' en el setting.py en la
parte de TEMPLATES -- OPTIONS -- context_procesors

"""

from django.conf import settings
from django.utils.translation import gettext as _
from django.db.utils import OperationalError

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide,
Schedule, Brand, Question, SampleImage, SampleVideo)

try:
    from store.models import Item
except (ImportError):
    pass





class Base:

    @classmethod
    def social_networks(self, request=None):
        try:
            return SocialNetwork.objects.all()
        except (OperationalError) as e:
            print(e)
        
    @classmethod
    def setting(self, request=None):
        try:
            return Setting.objects.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def advanced_setting(self, request=None):
        try:
            return AdvancedSetting.objects.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sliders(self, request=None):
        try:
            return Slide.objects.filter(is_active=True)
        except (OperationalError) as e:
            print(e)

    @classmethod
    def schedule(self, request=None):
        try:
            return Schedule.objects.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def brands(self, request=None):
        try:
            return Brand.objects.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def questions(self, request=None):
        try:
            return Question.objects.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_images(self, request=None):
        try:
            return SampleImage.objects.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_videos(self, request=None):
        try:
            return SampleVideo.objects.all()
        except (OperationalError) as e:
            print(e)



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