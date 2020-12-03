import datetime

from django.db import models
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
    website_name = models.CharField(_l("Nombre del sitio"), max_length=70, 
    help_text=_l("Nombre de este sitio. "))

    icon = models.ImageField(_("Icono del sitio"), blank=True, null=True, 
    upload_to="setting", help_text=_l("Imagen que aparecerá junto al título en "
    "la pestaña del navegador web. Esta imagen debe ser cuadrada, de no serlo "
    "se recortará para conseguir la dimensión requerida."))

    logo = models.ImageField(_l("Logo"), blank=True, null=True, 
    upload_to="setting")

    description = models.CharField(_l("Descripción"), max_length=200, blank=True,
    help_text=_l("Breve descripción del sitio."))

    # Cover.
    cover = models.ImageField(_l("Portada"), blank=True, null=True, 
    upload_to="setting",
    help_text=_l("Imagen de portada que se mostraráen la parte superior."))

    cover_height = models.IntegerField(_l("Portada tamaño"), default=256, 
    validators=[MinValueValidator(0), MaxValueValidator(512)],
    help_text=_l("Altura que tendrá la portada."))

    phone1 = models.CharField(_l("Central telefónica"), max_length=20, blank=True)
    
    phone2 = models.CharField(_l("Teléfono secundario"), max_length=20, blank=True)

    email = models.EmailField(_l("Correo electrónico"), blank=True)

    address = models.CharField(_l("Dirección principal"), max_length=256, blank=True)

    
    # About.

    about_image_cover = models.ImageField(_l("Acerca de: Portada"), blank=True, 
    upload_to="about")
    
    about_image_footer = models.ImageField(_l("Acerca de: Imagen pie de página"), 
    blank=True, upload_to="about")

    about_title = models.CharField(_l("Acerca de: Título"), max_length=70, blank=True)

    about_content = models.TextField(_l("Acerca de: Contenido"), blank=True)



    class Meta:
        verbose_name = _("Ajustes")

    
    def __str__(self):
        return _("Ajuste")

    
    def clean(self):
        # Solo existirá una configuración.
        if not self.pk:
            if Setting.objects.count():
                raise ValidationError(_("Ya existe una configuración. Puede "
                "modificar la configuración que ya está creada."))





class AdvancedSetting(models.Model):
    """
    Configuración avanzada del sitio destinada al proveedor.

    """



# class Navbar(models.Model):
#     """
#     Barra de navegación.
    
#     """
#     background_color = ColorField(verbose_name=_l("Color de fondo"), 
#     default="#FFFFFF")

#     background_opacity = models.IntegerField(_l("Opacidad del fondo"), 
#     default=1)
    
#     foreground_color = ColorField(_l("Color del texto"), default="#303030")

#     is_fixed = models.BooleanField(_l("Fijar"), default=True,
#     help_text=_l("Fija la barra de navegación en la parte superior."))

#     logo = models.ImageField(_l("Logo"), blank=True)




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
        "facebook": "/static/img/social/facebook.svg",
        "instagram": "/static/img/social/instagram.svg",
        "linkedin": "/static/img/social/linkedin.svg",
        "pinterest": "/static/img/social/pinterest.svg",
        "snapchat": "/static/img/social/snapchat.svg",
        "telegram": "/static/img/social/telegram.svg",
        "tumblr": "/static/img/social/tumblr.svg",
        "twitter": "/static/img/social/twitter.svg",
        "vkontakte": "/static/img/social/vk.svg",
        "whatsapp": "/static/img/social/whatsapp.svg",
        "youtube": "/static/img/social/youtube.svg",
    }

    social_network_name = models.CharField(_l("Red social"), max_length=20, 
    unique=True, choices=SOCIAL_NETWORK_CHOICES)

    url = models.URLField(_l("URL"), unique=True, 
    help_text=_l("Enlace hacia su perfil en esta red social."))

    index = models.IntegerField(_l("Indice"), default=0, 
    validators=[MinValueValidator(-99), MaxValueValidator(99)],
    help_text=_l("Ordena los links de las redes sociales acorde a este indice."))


    class Meta:
        verbose_name = _("Red social")
        verbose_name_plural = _("Redes sociales")
        ordering = ["index", "social_network_name"]

    
    def __str__(self):
        return self.social_network_name

    def GetImg(self):
        return self.SOCIAL_NETWORK_ICONS[self.social_network_name]
    





class Slide(models.Model):
    """
    Diapositiva para un carrusel de imágenes.
    
    """
    image = models.ImageField(_l("Imagen"), upload_to="slide")

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=200, blank=True)

    index = models.IntegerField(_l("Indice"), default=0, 
    validators=[MinValueValidator(-100), MaxValueValidator(100)],
    help_text=_l("Orden de las diapositivas."))

    is_active = models.BooleanField(_l("Activa"), default=True)


    class Meta:
        verbose_name = _("Diapositiva")
        verbose_name_plural = _("Diapositivas")
        ordering = ["index", "id"]

    
    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}. {self.title}"

    def clean(self):
        # Limitamos los registros de diapositivas a 100.
        if (not self.pk) and (Slide.objects.count() >= 100):
            raise ValidationError(_("Se ha alcanzado el número máximo de "
            "diapositivas registradas. Intente eliminar o modificar las que ya "
            "están registradas."))
        
    def GetImg(self):
        return self.image.url





class Schedule(models.Model):
    """
    Horario de servicio.

    """
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





class Brand(models.Model):
    """
    Marcas representadas.
    
    """
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


    class Meta:
        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")
        ordering = ["index"]

    
    def __str__(self):
        return self.name

    def GetImg(self):
        return self.image.url






class Question(models.Model):
    """
    Preguntas y respuestas.

    """
    question = models.CharField(_l("Pregunta"), max_length=100, unique=True)

    answer = models.CharField(_l("Respuesta"), max_length=700)


    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")

    
    def __str__(self):
        return self.question

    




class SampleImage(models.Model):
    """
    Imágen de muestra.
    
    """

    RECORD_LIMIT = 50 # Número máximo de registros que se pueden registrar.

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=700, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="sapleimage", 
    validators=[validate_image_size])

    index = models.IntegerField(_l("Indice"), default=0, help_text=_l("Orden "
    "en que será mostrada la imagen con respecto a otra."))


    class Meta:
        verbose_name = _("Imagen de muestra")
        verbose_name_plural = _("Imágenes de muestra")
        ordering = ["index"]

    
    def __str__(self):
        return self.title or f"Imágen: {self.id}"

    def clean(self):
        if SampleVideo.objects.count() >= self.RECORD_LIMIT:
            raise ValidationError(_("Se alcanzó el máximo de imágenes subidas."))





class SampleVideo(models.Model):
    """
    Video de muestra.
    
    """
    RECORD_LIMIT = 5 # Número máximo de registros que se pueden registrar.

    title = models.CharField(_l("Título"), max_length=70, blank=True)

    description = models.CharField(_l("Descripción"), max_length=700, blank=True)

    video = models.FileField(_l("Video"), upload_to="saplevideo",
    validators=[validate_video_size])

    index = models.IntegerField(_l("Indice"), default=0, help_text=_l("Orden "
    "en que será mostrado el video con respecto a otro."))


    class Meta:
        verbose_name = _("Video de muestra")
        verbose_name_plural = _("Videos de muestra")
        ordering = ["index"]

    
    def __str__(self):
        return self.title or f"Video: {self.id}"

    def clean(self):
        if SampleVideo.objects.count() >= self.RECORD_LIMIT:
            raise ValidationError(_("Se alcanzó el máximo de videos subidos."))