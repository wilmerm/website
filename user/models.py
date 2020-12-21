
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.urls import reverse_lazy
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from django.contrib.auth.hashers import makepassword


from fuente import text



# Obtiene el site actual.
get_current_site = Site.objects.get_current




class User(AbstractUser):
    """
    Usuario.
        
    """

    IMAGE_DEFAULT = "/static/img/icons/person-fill.svg"
   
    username_validator = UnicodeUsernameValidator()

    site = site = models.ForeignKey(Site, on_delete=models.PROTECT, 
    editable=False, default=get_current_site)

    phone1 = models.CharField(_l("Teléfono principal"), max_length=20, blank=True)

    phone2 = models.CharField(_l("Teléfono secundario"), max_length=20, blank=True)

    address = models.CharField(_l("Dirección"), max_length=500, blank=True)

    image_url = models.URLField(_l("Imagen de perfil desde URL"), blank=True)

    google_userid = models.CharField(max_length=256, blank=True, editable=False)

    # Cuando el usuario es registrado a través de la API de Google (Por ejemplo).
    # Le establecemos una contraseña aleatoria de 10 dígitos que luego podrá
    # cambiar. Aquí la almacenamos como referencia para poder enviarsela, al 
    # usuario recientemente registrado, por correo, etc. 
    initial_password = models.CharField(
        _l("Contraseña inicial establecida por el sistema"), blank=True,
        max_length=10)


    objects = UserManager()
    on_site = CurrentSiteManager()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("site", "email"), 
                name="unique_user_on_site"),
        ]


    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse_lazy("user-profile")
    
    def clean(self):

        # Creación de un nuevo usuario.
        if (not self.pk):
            self.site = get_current_site()
            # Al crear un usuario nuevo, si no se especifica el email, se tomará
            # el nombre de usuario que se indicó (el nombre de usuario será
            # remplazado en save() por '{site__id}_{pk}'), el cual deberá ser 
            # un email válido.
            if not self.email:
                if not self.username:
                    raise ValidationError(
                        _("Debe indicar su correo electrónico."))
                
                self.email = self.username

        # En esta parte dejamos que Django realice su validación.
        super().clean() # self.__class__.objects.normalize_email(self.email)

        # El email lógicamente es obligatorio.
        if not self.email:
            raise ValidationError(_("Debe indicar un email válido."))

        # El email debe ser único para cada site.
        if User.objects.filter(site=self.site, email=self.email).exclude(pk=self.pk):
            raise ValidationError(_("Ya existe otro usuario con este correo "
            "electrónico. Puede intentar iniciar sesión en su lugar."))


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Debido a que se está trabajando con varios sitios en una misma 
        # base de datos y el nombre de usuario debe ser único, pues 
        # implementamos un backend de autentificación que permite iniciar 
        # sesión con el email.Entonces el nombre de usuario lo estable el 
        # sistema y no será mostrado al usuario, en le haremos creer que el 
        # nombre de usuario es su email, el cual será único para cada sitio.
        self.username = "%s_%s" % (self.site.id, self.pk)
        
        return super().save(*args, **kwargs)
    
    def get_full_name(self):
        full_name = super().get_full_name()
        if not full_name:
            full_name = self.email.split("@")[0].upper()
        return full_name

    def GetImg(self):
        if not self.image_url:
            return self.IMAGE_DEFAULT
        return self.image_url








        