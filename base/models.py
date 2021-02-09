import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator)

from colorfield.fields import ColorField

from user.models import User



def validate_video_size(value):
    """Validador de máximo size permitido en subida de archivos."""
    size = 50 * 1024 * 1024 # 50 MB
    filesize = value.size
    
    if filesize > size:
        raise ValidationError(f"El valor máximo del archivo es "
    f"{size/1024/1024} MB, este tiene {round(filesize/1024/1024)} MB")
    return value


def validate_image_size(value):
    """Validador de máximo size permitido en subida de archivos."""
    size = 5 * 1024 * 1024 # 5 MB
    filesize = value.size
    
    if filesize > size:
        raise ValidationError(f"El valor máximo del archivo es "
    f"{size/1024/1024} MB, este tiene {round(filesize/1024/1024)} MB")
    return value


class Setting(models.Model):
    """
    Configuración del sitio.
    """

    REGISTRATION_MESSAGE_DEFAULT = _l("Si aún no estás registrado, por favor, "
    "cree una cuenta con nosotros.")

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    website_name = models.CharField(_l("Nombre del sitio"), max_length=70, 
    help_text=_l("Nombre de este sitio. "))

    icon = models.ImageField(_("Icono del sitio"), blank=True, null=True, 
    upload_to="setting", help_text=_l("Imagen que aparecerá junto al título en "
    "la pestaña del navegador web. Esta imagen debe ser cuadrada, de no serlo "
    "se recortará para conseguir la dimensión requerida."))

    logo = models.ImageField(_l("Logo"), blank=True, null=True, 
    upload_to="setting")

    description = models.CharField(_l("Descripción"), max_length=200, 
    blank=True, help_text=_l("Breve descripción del sitio."))

    # Cover.

    cover = models.ImageField(_l("Portada"), blank=True, null=True, 
    upload_to="setting",
    help_text=_l("Imagen de portada que se mostraráen la parte superior."))

    cover_height = models.IntegerField(_l("Portada tamaño"), default=256, 
    validators=[MinValueValidator(0), MaxValueValidator(512)],
    help_text=_l("Altura que tendrá la portada."))

    # Contacts, address and schedule

    phone1 = models.CharField(_l("Central telefónica"), max_length=20, 
    blank=True)
    
    phone2 = models.CharField(_l("Teléfono secundario"), max_length=20, 
    blank=True)

    email = models.EmailField(_l("Correo electrónico"), blank=True)

    address = models.CharField(_l("Dirección principal"), max_length=256, 
    blank=True)

    schedule = models.CharField(_l("Horario de trabajo"), max_length=150,
    blank=True)

    # About.

    about_title = models.CharField(_l("Acerca de: Título"), max_length=70, 
    blank=True)

    about_content = models.TextField(_l("Acerca de: Contenido"), blank=True)

    about_image_cover = models.ImageField(_l("Acerca de: Portada"), blank=True, 
    upload_to="about")
    
    about_image_footer = models.ImageField(_l("Acerca de: Imagen pie de página"), 
    blank=True, upload_to="about")

    # Information.

    information_title = models.CharField(_l("Información: Título"), 
    max_length=70, blank=True, default=_l("Póngase en contacto con nostros"))

    information_content = models.TextField(_l("Información: Contenido"), 
    blank=True, default=_l("Póngase en contacto con nostros ahora mismo."))

    # Registration.

    registration_message = models.TextField(_l("Mensaje para nuevos registros"),
    blank=True, default=REGISTRATION_MESSAGE_DEFAULT, 
    help_text=_l("Mensaje que se muestra a los usuarios en la página de "
    "inicio de sesión, invitándolos a que, de no estar registrados, que se "
    "registren."))

    # Others.

    embed_map_html = models.TextField(_l("Código inserción de mapa"), blank=True, 
    help_text=_l("Código HTML/Javascript que se mostrará en una de las "
    "partes de la página principal como el mapa."))

    embed_promo_url = models.URLField(_l("URL de promoción incrustrada"), 
    blank=True, help_text=_l("URL del contenido externo que desea mostrar como "
    "promoción en la página principal. Esta url puede bien ser la url de un "
    "video en Youtube, una imagen, o un contenido html."))

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("Ajustes")
        verbose_name_plural = _l("Ajustes")

    def __str__(self):
        return _(f"Ajustes para {self.site}")

    def clean(self):
        # Solo existirá una configuración por sitio.
        current_site = Site.objects.get_current()

        if not self.pk:
            if Setting.objects.filter(site=current_site).count():
                raise ValidationError(_("Ya existe una configuración para "
                f"{current_site}. Puede modificarla"))
            self.site = Site.objects.get_current()

    @classmethod
    def GetForCurrentSite(self):
        """Obtiene la configuración del sitio actual."""
        return Setting.objects.filter(site=Site.objects.get_current()).last()


class AdvancedSetting(models.Model):
    """
    Configuración avanzada del sitio destinada al proveedor.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False, 
    blank=True, null=True)

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("configuración avanzada")
        verbose_name_plural = _l("configuración avanzada")

    def __str__(self):
        return f"Configuración avanzada para {self.site}"

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetForCurrentSite(self):
        """Obtiene la configuración avanzada del sitio actual."""
        return AdvancedSetting.objects.filter(
            site=Site.objects.get_current()).last()


class SocialNetwork(models.Model):
    """
    Redes sociales.
    """

    SOCIAL_NETWORK_CHOICES = (
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("pinterest", "Pinterest"),
        ("snapchat", "Snapchat"),
        ("telegram", "Telegram"),
        ("tumblr", "Tumblr"),
        ("twitter", "Twitter"),
        ("vkontakte", "Vkontakte"),
        ("whatsapp", "Whatsapp"),
        ("youtube", "Youtube"),
    )
    SOCIAL_NETWORK_ICONS = {
        "facebook": "/static/img/social/facebook-rounded-fill.svg",
        "instagram": "/static/img/social/instagram-rounded-fill.svg",
        "linkedin": "/static/img/social/linkedin.svg-rounded-fill",
        "pinterest": "/static/img/social/pinterest-rounded-fill.svg",
        "snapchat": "/static/img/social/snapchat-rounded-fill.svg",
        "telegram": "/static/img/social/telegram-rounded-fill.svg",
        "tumblr": "/static/img/social/tumblr-rounded-fill.svg",
        "twitter": "/static/img/social/twitter-rounded-fill.svg",
        "vkontakte": "/static/img/social/vk-rounded-fill.svg",
        "whatsapp": "/static/img/social/whatsapp-rounded-fill.svg",
        "youtube": "/static/img/social/youtube-rounded-fill.svg",
    }

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False, 
    blank=True, null=True)

    social_network_name = models.CharField(_l("red social"), max_length=20, 
    choices=SOCIAL_NETWORK_CHOICES)

    url = models.URLField(_l("URL"), unique=True, 
    help_text=_l("enlace hacia su perfil en esta red social."))

    index = models.IntegerField(_l("indice"), default=0, 
    validators=[MinValueValidator(-99), MaxValueValidator(99)],
    help_text=_l("ordena los links de las redes sociales acorde a este indice."))

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("red social")
        verbose_name_plural = _l("redes sociales")
        ordering = ["index", "social_network_name"]

    def __str__(self):
        return self.social_network_name

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    def GetImg(self):
        return self.SOCIAL_NETWORK_ICONS[self.social_network_name]

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return SocialNetwork.objects.filter(site=Site.objects.get_current())
    

class Slide(models.Model):
    """
    Diapositiva para un carrusel de imágenes.
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False, 
    blank=True, null=True)

    image = models.ImageField(_l("imagen"), upload_to="slide")

    title = models.CharField(_l("título"), max_length=70, blank=True)

    description = models.CharField(_l("descripción"), max_length=200, blank=True)

    index = models.IntegerField(_l("indice"), default=0, 
    validators=[MinValueValidator(-100), MaxValueValidator(100)],
    help_text=_l("orden de las diapositivas."))

    is_active = models.BooleanField(_l("activa"), default=True)

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("diapositiva")
        verbose_name_plural = _l("diapositivas")
        ordering = ["index", "id"]
    
    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}. {self.title}"

    def clean(self):
        # Limitamos los registros de diapositivas a 100.
        if not self.pk:
            if Slide.objects.count() >= 100:
                raise ValidationError(_("Se ha alcanzado el número máximo de "
                "diapositivas registradas. Intente eliminar o modificar las "
                "que ya están registradas."))
            
            self.site = Site.objects.get_current()
        
    def GetImg(self):
        return self.image.url

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return Slide.objects.filter(site=Site.objects.get_current())


class Schedule(models.Model):
    """
    Horario de servicio.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False, 
    blank=True, null=True)

    monday = models.BooleanField(_l("Lunes"), default=True)

    monday_ini = models.TimeField(_l("Lunes: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    monday_end = models.TimeField(_l("Lunes: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    tuesday = models.BooleanField(_l("Tuesday"), default=True)

    tuesday_ini = models.TimeField(_l("Tuesday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    tuesday_end = models.TimeField(_l("Tuesday: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    wednesday = models.BooleanField(_l("Wednesday"), default=True)

    wednesday_ini = models.TimeField(_l("Wednesday: desde"), null=True, 
    blank=True, default=datetime.time(8, 0))

    wednesday_end = models.TimeField(_l("Wednesday: hasta"), null=True, 
    blank=True, default=datetime.time(18, 0))


    thursday = models.BooleanField(_l("Thursday"), default=True)

    thursday_ini = models.TimeField(_l("Thursday: desde"), null=True, 
    blank=True, default=datetime.time(8, 0))

    thursday_end = models.TimeField(_l("Thursday: hasta"), null=True, 
    blank=True, default=datetime.time(18, 0))


    friday = models.BooleanField(_l("Friday"), default=True)

    friday_ini = models.TimeField(_l("Friday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    friday_end = models.TimeField(_l("Friday: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    saturday = models.BooleanField(_l("Saturday"), default=True)

    saturday_ini = models.TimeField(_l("Saturday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    saturday_end = models.TimeField(_l("Saturday: hasta"), null=True, blank=True,
    default=datetime.time(12, 0))


    sunday = models.BooleanField(_l("Sunday"), default=False)

    sunday_ini = models.TimeField(_l("Sunday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    sunday_end = models.TimeField(_l("Sunday: hasta"), null=True, blank=True,
    default=datetime.time(12, 0))

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("horario de servicio")
        verbose_name_plural = _l("horario de servicio")

    def __str__(self):
        return self._meta.verbose_name

    def clean(self):
        # Solo habrá un único registro.
        if not self.pk:
            if Schedule.objects.count():
                raise ValidationError(_("Ya existe el horario."))

            self.site = Site.objects.get_current()

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return Schedule.objects.filter(site=Site.objects.get_current())

    def GetRangeForDay(self):
        return {
            "monday": list(range(self.monday_ini, self.monday_end)), 
            "tuesday": list(range(self.tuesday_ini, self.tuesday_end)),
            "wednesday": list(range(self.wednesday_ini, self.wednesday_end)),
            "thursday": list(range(self.thursday_ini, self.thursday_end)),
            "friday": list(range(self.friday_ini, self.friday_end)),
            "saturday": list(range(self.saturday_ini, self.saturday_end)),
            "sunday": list(range(self.sunday_ini, self.sunday_end))
        }

    def GetRangeTimes(self):
        tmin = self.GetMinTime()
        tmax = self.GetMaxTime()
        return list(range(tmin, tmax))

    def GetMinTime(self):
        """Obtiene la hora más baja registrada."""
        return min(self.GetAllTimes())
    
    def GetMaxTime(self):
        """Obtiene la hora más alta registrada."""
        return max(self.GetAllTimes())

    def GetAllTimes(self):
        return [
            self.monday_ini, self.monday_end, 
            self.tuesday_ini, self.tuesday_end,
            self.wednesday_ini, self.wednesday_end,
            self.thursday_ini, self.thursday_end,
            self.friday_ini, self.friday_end,
            self.saturday_ini, self.saturday_end,
            self.sunday_ini, self.sunday_end
        ]


class BrandRepresented(models.Model):
    """
    Marcas representadas.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    name = models.CharField(_l("nombre"), max_length=100)

    image = models.ImageField(_l("imagen"), upload_to="brand", 
    help_text=_l("logo de la marca. Se recomienda una imagen cuadrada, con fondo "
    "transparente, en formato PNG o GIF."))

    cover = models.ImageField(_l("portada"), upload_to="brand", blank=True,
    help_text=_l("imagen que se usará como fondo para ambientar la sección de "
    "la marca. Se recomienda una imagen en alta resolución, con dimensión "
    "rectangular más ancha que alta."))

    url = models.URLField(_l("web site"), blank=True, 
    help_text=_l("dirección URL del sitio web de la marca."))

    index = models.IntegerField(_l("indice"), default=0, 
    help_text=_l("determina la posición que ocupará la marca cuando se muestre "
    "junto a las demás. Las marcas se mostrarán en orden en función de su "
    "indice, de mejor a mayor."))

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("marca")
        verbose_name_plural = _l("marcas")
        ordering = ["index"]

    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    def GetImg(self):
        return self.image.url

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return BrandRepresented.objects.filter(site=Site.objects.get_current())


class Question(models.Model):
    """
    Preguntas y respuestas.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    question = models.CharField(_l("pregunta"), max_length=100, unique=True)

    answer = models.CharField(_l("respuesta"), max_length=700)

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("pregunta")
        verbose_name_plural = _l("preguntas")
    
    def __str__(self):
        return self.question

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return Question.objects.filter(site=Site.objects.get_current())

    
class SampleImage(models.Model):
    """
    Imágen de muestra.
    """

    RECORD_LIMIT = 50 # Número máximo de registros que se pueden registrar.

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    title = models.CharField(_l("título"), max_length=70, blank=True)

    description = models.CharField(_l("descripción"), max_length=700, blank=True)

    image = models.ImageField(_l("imágen"), upload_to="sapleimage", 
    validators=[validate_image_size])

    index = models.IntegerField(_l("indice"), default=0, help_text=_l("orden "
    "en que será mostrada la imagen con respecto a otra."))

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("imagen de muestra")
        verbose_name_plural = _l("imágenes de muestra")
        ordering = ["index"]
    
    def __str__(self):
        return self.title or f"Imágen: {self.id}"

    def clean(self):
        if SampleVideo.objects.filter(
            site=Site.objects.get_current()).count() > self.RECORD_LIMIT:
            raise ValidationError(_("Se alcanzó el máximo de imágenes subidas."))
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return SampleImage.objects.filter(site=Site.objects.get_current())


class SampleVideo(models.Model):
    """
    Video de muestra.
    """

    RECORD_LIMIT = 5 # Número máximo de registros que se pueden registrar.

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    title = models.CharField(_l("título"), max_length=70, blank=True)

    description = models.CharField(_l("descripción"), max_length=700, blank=True)

    video = models.FileField(_l("video"), upload_to="saplevideo",
    validators=[validate_video_size])

    index = models.IntegerField(_l("indice"), default=0, help_text=_l("orden "
    "en que será mostrado el video con respecto a otro."))

    objects = models.Manager()

    on_site = CurrentSiteManager()
    
    class Meta:
        verbose_name = _l("video de muestra")
        verbose_name_plural = _l("videos de muestra")
        ordering = ["index"]

    def __str__(self):
        return self.title or f"Video: {self.id}"

    def clean(self):
        if SampleVideo.objects.filter(
            site=Site.objects.get_current()).count() > self.RECORD_LIMIT:
            raise ValidationError(_("Se alcanzó el máximo de videos subidos."))
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetAllForCurrentSite(self):
        """Obtiene los registros para el sitio actual."""
        return SampleVideo.objects.filter(site=Site.objects.get_current())


class VisitCounter(models.Model):
    """
    Contador de visitas a páginas.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    urlpath = models.CharField(_l("URL path"), max_length=200)

    date = models.DateField(verbose_name=_l("fecha"), 
    auto_now=True)

    count = models.IntegerField(_l("cantidad"), default=0)

    objects = models.Manager()

    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("visita")
        verbose_name_plural = _l("visitas")
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(fields=("site", "urlpath", "date"), 
            name="unique_visitcounter"),
        ]

    def __str__(self):
        return f"{self.date}: {self.site}{self.urlpath}"

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def __total(self, queryset) -> int:
        return queryset.aggregate(models.Sum("count"))["cont__sum"]

    @classmethod
    def GetTotalOnSite(self, site: Site=None) -> int:
        """
        Obtiene la sumatoria de visitas en el sitio indicado.

        Parameters:
            site (django.sites.models.Site): default self.site or current_site.

        """
        site = site or self.site or Site.objects.get_current()

        if site:
            qs = VisitCounter.objects.filter(site=site)
        else:
            qs = VisitCounter.objects.all()
        return self.__total(qs)

    @classmethod
    def GetTotalOnPath(self, site: Site=None, urlpath: str=None) -> int:
        """
        Obtiene la sumatoria de visitas en el sitio y url indicada.

        De no especificarse algún parámetro y ser esta una instancia, se tomarán
        los valores de la instancia.

        Parameters:
            site (django.sites.models.Site): default self.site.
            
            urlpath (str): default self.urlpath.
        
        """
        site = site or self.site or Site.objects.get_current()
        urlpath = urlpath or self.urlpath

        if (not site) or (not urlpath):
            raise ValueError("Debe indicar el 'site' y el 'urlpath' parámetros.")

        qs = VisitCounter.objects.filter(site=site, urlpath=urlpath)
        return self.__total(qs)

    @classmethod
    def GetTotalOnDate(self, site: Site=None, urlpath: str=None, 
        date: timezone=None) -> int:
        """
        Obtiene la sumatoria de visitas en el sitio, url y fecha indicada.

        De no especificarse algún parámetro y ser esta una instancia, se tomarán
        los valores de la instancia, en el caso de la fecha será la de hoy.

        Parameters:
            site (django.sites.models.Site): default self.site.
            
            urlpath (str): default self.urlpath.

            date (datetime.date): default timezone.now.
        
        """
        site = site or self.site or Site.objects.get_current()
        urlpath = urlpath or self.urlpath
        date = date or timezone.now()

        if (not site) or (not urlpath) or (not date):
            raise ValueError(
                "Debe indicar los parámetros 'site', 'urlpath' y 'date'")
        qs = VisitCounter.objects.filter(site=site, urlpath=urlpath, date=date)
        return self.__total(qs)

    @classmethod
    def on_today(self, urlpath: str=None):
        """
        Obtiene un queryset con todas las visitas de hoy, o una única instancia
        de la visita de hoy a una página especifica si se indica 'urlpath'.

        Nota: las visitas son únicas para cada site, urlpath, date.
        Si se indica 'urlpath' y no hay resultados, lanzará 'DoesNotExist'.

        """
        if urlpath:
            return VisitCounter.on_site.get(urlpath=urlpath, date=timezone.now())
        return VisitCounter.on_site.filter(date=timezone.now())


class Message(models.Model):
    """
    Mensaje de los usuarios.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  
    blank=True, null=True)

    name = models.CharField(_l("nombre"), max_length=100, blank=True)

    email = models.EmailField(_l("email"), blank=True)

    phone = models.CharField(_l("teléfono"), max_length=50, blank=True)

    address = models.CharField(_l("dirección"), max_length=200, blank=True)

    service_type = models.CharField(_l("servicio"), max_length=100, blank=True)

    warranty = models.CharField(_l("garantía"), max_length=100, blank=True)

    message = models.CharField(_l("mensaje"), max_length=700, blank=True)

    date = models.DateTimeField(_l("fecha"), auto_now_add=True, editable=False)

    read_date = models.DateTimeField(_l("fecha de leído"), null=True, blank=True)

    objects = models.Manager()

    on_site = CurrentSiteManager()
    
    class Meta:
        verbose_name = _l("mensaje")
        verbose_name_plural = _l("mensajes")
        ordering = ["-date", "email"]

    def __str__(self):
        return f"{self.date}: {self.email}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.site = Site.objects.get_current()
        return super().save(*args, **kwargs)

    