
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.db.models.signals import post_save
from django.dispatch import receiver





class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-
    authentication-removing-the-username
    
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class User(AbstractUser):
    """
    Usuario.

    El usuario será creado para que exista en todos los sitios, lo que validará
    en que sitio puede o iniciar lo determinará el perfil (Profile).
    
    """

    # Eliminando el campo de nombre de usuario .
    # Hacer que el campo de correo electrónico sea obligatorio y único.
    # Decirle a Django que usará el campo de correo electrónico como USERNAME_FIELD.
    # Eliminando el campo de correo electrónico de la configuración de 
    # REQUIRED_FIELDS (se incluye automáticamente como USERNAME_FIELD).
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/

    username = None

    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager() ## This is the new line in the User model. ##


    def GetProfile(self, site=None):
        """
        Obtiene el perfil asignado a este usuario en el sitio indicado o actual.

        """
        site = site or Site.objects.get_current()
        return Profile.objects.get(site=site, user=self)

    def GetProfileOrCreate(self, site=None):
        """
        Obtiene el perfil asignado a este usuario en el sitio indicado o actual.

        Si el perfil no exite será creado con los datos básicos.
        
        """
        site = site or Site.objects.get_current()
        try:
            return self.GetProfile(site=site)
        except (Profile.DoesNotExist):
            profile = Profile(user=self, site=site)
            profile.clean()
            profile.save()
            return profile

    def profile(self):
        """
        Igual que self.GetProfileOrCreate(site=None), para uso en plantillas.

        """
        return self.GetProfileOrCreate()




class Profile(models.Model):
    """
    Perfil de usuario para cada sitio.
    
    """
    site = models.OneToOneField(Site, on_delete=models.PROTECT, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    address = models.CharField(_l("Dirección"), max_length=700, blank=True)

    phone1 = models.CharField(_l("Teléfono principal"), max_length=20, 
    blank=True)
    
    phone2 = models.CharField(_l("Teléfono secundario"), max_length=20, 
    blank=True)

    is_active = models.BooleanField(_l("Perfil activo"), default=False)

    create_date = models.DateTimeField(_("Creación"), auto_now_add=True,
    editable=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["site", "user"], name="unique_profile")
        ]

    
    def __str__(self):
        return str(self.user)
