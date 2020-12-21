import datetime

from django.db import models
from django.contrib.sites.models import Site, SiteManager
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator)

from colorfield.fields import ColorField





def validate_video_size(value):
    """
    Validador de máximo size permitido en subida de archivos.

    """
    size = 50 * 1024 * 1024 # 50 MB
    filesize = value.size
    
    if filesize > size:
        raise ValidationError(f"El valor máximo del archivo es "
    f"{size/1024/1024} MB, este tiene {round(filesize/1024/1024)} MB")

    return value




def validate_image_size(value):
    """
    Validador de máximo size permitido en subida de archivos.

    """
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


    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, 
    null=True)

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
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Ajustes")
        verbose_name_plural = _("Ajustes")

    
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
        """
        Obtiene la configuración del sitio actual.

        """
        return Setting.objects.filter(site=Site.objects.get_current()).last()





class AdvancedSetting(models.Model):
    """
    Configuración avanzada del sitio destinada al proveedor.

    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Configuración avanzada")
        verbose_name_plural = _("Configuración avanzada")

    
    def __str__(self):
        return f"Configuración avanzada para {self.site}"

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetForCurrentSite(self):
        """
        Obtiene la configuración avanzada del sitio actual.
        
        """
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

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    social_network_name = models.CharField(_l("Red social"), max_length=20, 
    choices=SOCIAL_NETWORK_CHOICES)

    url = models.URLField(_l("URL"), unique=True, 
    help_text=_l("Enlace hacia su perfil en esta red social."))

    index = models.IntegerField(_l("Indice"), default=0, 
    validators=[MinValueValidator(-99), MaxValueValidator(99)],
    help_text=_l("Ordena los links de las redes sociales acorde a este indice."))

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Red social")
        verbose_name_plural = _("Redes sociales")
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
        """
        Obtiene los registros para el sitio actual.
        
        """
        return SocialNetwork.objects.filter(site=Site.objects.get_current())
    





class Slide(models.Model):
    """
    Diapositiva para un carrusel de imágenes.
    
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    image = models.ImageField(_l("Imagen"), upload_to="slide")

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=200, blank=True)

    index = models.IntegerField(_l("Indice"), default=0, 
    validators=[MinValueValidator(-100), MaxValueValidator(100)],
    help_text=_l("Orden de las diapositivas."))

    is_active = models.BooleanField(_l("Activa"), default=True)

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Diapositiva")
        verbose_name_plural = _("Diapositivas")
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
        """
        Obtiene los registros para el sitio actual.
        
        """
        return Slide.objects.filter(site=Site.objects.get_current())





class Schedule(models.Model):
    """
    Horario de servicio.

    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    monday = models.BooleanField(_l("Lunes"), default=True)

    monday_ini = models.TimeField(_("Lunes: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    monday_end = models.TimeField(_("Lunes: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    tuesday = models.BooleanField(_l("Tuesday"), default=True)

    tuesday_ini = models.TimeField(_("Tuesday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    tuesday_end = models.TimeField(_("Tuesday: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    wednesday = models.BooleanField(_l("Wednesday"), default=True)

    wednesday_ini = models.TimeField(_("Wednesday: desde"), null=True, 
    blank=True, default=datetime.time(8, 0))

    wednesday_end = models.TimeField(_("Wednesday: hasta"), null=True, 
    blank=True, default=datetime.time(18, 0))


    thursday = models.BooleanField(_l("Thursday"), default=True)

    thursday_ini = models.TimeField(_("Thursday: desde"), null=True, 
    blank=True, default=datetime.time(8, 0))

    thursday_end = models.TimeField(_("Thursday: hasta"), null=True, 
    blank=True, default=datetime.time(18, 0))


    friday = models.BooleanField(_l("Friday"), default=True)

    friday_ini = models.TimeField(_("Friday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    friday_end = models.TimeField(_("Friday: hasta"), null=True, blank=True,
    default=datetime.time(18, 0))


    saturday = models.BooleanField(_l("Saturday"), default=True)

    saturday_ini = models.TimeField(_("Saturday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    saturday_end = models.TimeField(_("Saturday: hasta"), null=True, blank=True,
    default=datetime.time(12, 0))


    sunday = models.BooleanField(_l("Sunday"), default=False)

    sunday_ini = models.TimeField(_("Sunday: desde"), null=True, blank=True,
    default=datetime.time(8, 0))

    sunday_end = models.TimeField(_("Sunday: hasta"), null=True, blank=True,
    default=datetime.time(12, 0))

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Horario de servicio")
        verbose_name_plural = _("Horario de servicio")

    
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
        """
        Obtiene los registros para el sitio actual.
        
        """
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
        """
        Obtiene la hora más baja registrada.
        """
        return min(self.GetAllTimes())
    
    def GetMaxTime(self):
        """
        Obtiene la hora más alta registrada.
        """
        return max(self.GetAllTimes())

    def GetAllTimes(self):
        return [
            self.monday_ini, self.monday_end, 
            self.tuesday_ini, self.tuesday_end,
            self.wednesday_ini, self.wednesday_end,
            self.thursday_ini, self.thursday_end,
            self.friday_ini, self.friday_end,
            self.saturday_ini, self.saturday_end,
            self.sunday_ini, self.sunday_end]





class BrandRepresented(models.Model):
    """
    Marcas representadas.
    
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    name = models.CharField(_l("Nombre"), max_length=100)

    image = models.ImageField(_l("Imagen"), upload_to="brand", 
    help_text=_l("Logo de la marca. Se recomienda una imagen cuadrada, con fondo "
    "transparente, en formato PNG o GIF."))

    cover = models.ImageField(_l("Portada"), upload_to="brand", blank=True,
    help_text=_l("Imagen que se usará como fondo para ambientar la sección de "
    "la marca. Se recomienda una imagen en alta resolución, con dimensión "
    "rectangular más ancha que alta."))

    url = models.URLField(_l("Web Site"), blank=True, 
    help_text=_l("Dirección URL del sitio web de la marca."))

    index = models.IntegerField(_l("Indice"), default=0, 
    help_text=_l("Determina la posición que ocupará la marca cuando se muestre "
    "junto a las demás. Las marcas se mostrarán en orden en función de su "
    "indice, de mejor a mayor."))

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")
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
        """
        Obtiene los registros para el sitio actual.
        
        """
        return BrandRepresented.objects.filter(site=Site.objects.get_current())





class Question(models.Model):
    """
    Preguntas y respuestas.

    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    question = models.CharField(_l("Pregunta"), max_length=100, unique=True)

    answer = models.CharField(_l("Respuesta"), max_length=700)

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")

    
    def __str__(self):
        return self.question

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

    @classmethod
    def GetAllForCurrentSite(self):
        """
        Obtiene los registros para el sitio actual.
        
        """
        return Question.objects.filter(site=Site.objects.get_current())

    




class SampleImage(models.Model):
    """
    Imágen de muestra.
    
    """

    RECORD_LIMIT = 50 # Número máximo de registros que se pueden registrar.

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=700, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="sapleimage", 
    validators=[validate_image_size])

    index = models.IntegerField(_l("Indice"), default=0, help_text=_l("Orden "
    "en que será mostrada la imagen con respecto a otra."))

    objects = models.Manager()
    on_site = SiteManager()

    class Meta:
        verbose_name = _("Imagen de muestra")
        verbose_name_plural = _("Imágenes de muestra")
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
        """
        Obtiene los registros para el sitio actual.
        
        """
        return SampleImage.objects.filter(site=Site.objects.get_current())





class SampleVideo(models.Model):
    """
    Video de muestra.
    
    """
    RECORD_LIMIT = 5 # Número máximo de registros que se pueden registrar.

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,  blank=True, null=True)

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=700, blank=True)

    video = models.FileField(_l("Video"), upload_to="saplevideo",
    validators=[validate_video_size])

    index = models.IntegerField(_l("Indice"), default=0, help_text=_l("Orden "
    "en que será mostrado el video con respecto a otro."))

    objects = models.Manager()
    on_site = SiteManager()
    
    class Meta:
        verbose_name = _("Video de muestra")
        verbose_name_plural = _("Videos de muestra")
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
        """
        Obtiene los registros para el sitio actual.
        
        """
        return SampleVideo.objects.filter(site=Site.objects.get_current())