"""
Esto hace que todas las views de todas las aplicaciones, hereden estas
variables en su contexto para que todas las plantillas dispongan de esto
sin tener que desclararlas en las views.

Es necesario agregar 'base.context_processors.[NAME]' en el setting.py en la
parte de TEMPLATES -- OPTIONS -- context_procesors

"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from django.db.utils import OperationalError

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide,
    Schedule, BrandRepresented, Question, SampleImage, SampleVideo, Message, 
    VisitCounter)

try:
    from store.models import Item, StoreSetting
except (ImportError):
    pass



class Base:
    """
    Métodos abreviadas para la aplicación 'base'.
    """

    def __str__(self):
        return str(self.setting()) or "base"

    @classmethod
    def social_networks(cls, request=None):
        try:
            return SocialNetwork.on_site.all()
        except (OperationalError) as e:
            print(e)
        
    @classmethod
    def setting(cls, request=None):
        try:
            return Setting.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def advanced_setting(cls, request=None):
        try:
            return AdvancedSetting.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sliders(cls, request=None):
        try:
            return Slide.on_site.filter(is_active=True)
        except (OperationalError) as e:
            print(e)

    @classmethod
    def schedule(cls, request=None):
        try:
            return Schedule.on_site.last()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def brands(cls, request=None):
        try:
            return BrandRepresented.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def questions(cls, request=None):
        try:
            return Question.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_images(cls, request=None):
        try:
            return SampleImage.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def sample_images_dict(cls, request=None):
        qs = SampleImage.on_site.all() or []
        return {e.index:e for e in qs}

    @classmethod
    def sample_videos(cls, request=None):
        try:
            return SampleVideo.on_site.all()
        except (OperationalError) as e:
            print(e)

    @classmethod
    def message_class(cls):
        return Message

    @classmethod
    def visit_counter_class(cls):
        return VisitCounter


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
    def items(cls, request=None):
        try:
            return Item.on_site.filter(is_active=True)
        except (NameError) as e:
            print(e)

    @classmethod
    def setting(cls, request=None):
        try:
            return StoreSetting.on_site.last()
        except (NameError) as e:
            print(e)

    @classmethod
    def featured_items(cls, request=None):
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