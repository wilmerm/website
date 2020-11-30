import datetime

from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator)

from colorfield.fields import ColorField

from fuente import text



class Item(models.Model):
    """
    Artículo.
    
    """

    IMG_DEFAULT = "/static/img/base/articulo.svg"


    codename = models.CharField(_l("Referencia"), max_length=30, unique=True)

    name = models.CharField(_l("Nombre"), max_length=50, unique=True)

    description = models.CharField(_l("Descripción"), max_length=700, 
    blank=True)

    image1 = models.ImageField(_l("Imágen 1"), upload_to="store/item/", 
    blank=True)

    image2 = models.ImageField(_l("Imágen 2"), upload_to="store/item/", 
    blank=True)

    image3 = models.ImageField(_l("Imágen 3"), upload_to="store/item/", 
    blank=True)

    color1 = ColorField(_l("Color principal"), blank=True)

    color2 = ColorField(_l("Color secundario"), blank=True)

    weight = models.DecimalField(_l("Peso"), max_digits=17, decimal_places=2,
    null=True, blank=True)

    weight_type = models.CharField(_l("Peso (tipo)"), max_length=50, blank=True,
    help_text=_l("Indique el tipo de medida para el peso indicado (Kg, Lbr, "
    "Onz, ...)."))

    volumen = models.DecimalField(_l("Volumen"), max_digits=17, 
    decimal_places=2, null=True, blank=True)

    volumen_type = models.CharField(_l("Volumen (tipo)"), max_length=50, 
    blank=True, help_text=_l("Indique el tipo de medida para el volumen "
    "indicado (Ejemplo 'metro cúbico')."))

    length_width = models.DecimalField(_l("Longitud de ancho"), max_digits=17, 
    decimal_places=2, null=True, blank=True)

    length_height = models.DecimalField(_l("Longitud de alto"), max_digits=17, 
    decimal_places=2, null=True, blank=True)

    length_depth = models.DecimalField(_l("Longitud de profundidad"), 
    max_digits=17, decimal_places=2, null=True, blank=True)

    length_type = models.CharField(_l("Longitud (tipo)"), max_length=50, 
    blank=True, help_text=_l("Indique el tipo de medida para las longitudes "
    "indicadas (Ejemplo 'metro')."))

    material = models.CharField(_l("Material"), max_length=50, blank=True, 
    help_text=_l("Tipo de material principal del cual está constituído "
    "(Ejemplo 'plástico')."))

    price = models.DecimalField(_l("Precio"), max_digits=17, 
    decimal_places=2, null=True, blank=True) 

    is_active = models.BooleanField(_l("Activo"), default=True,
    help_text=_l("El artículo estará o no visible para la venta."))

    is_featured = models.BooleanField(_l("Destacado"), default=False,
    help_text=_l("El artículo aparecerá en los primeros lugares de la tienda."))


    # Inventario.

    available = models.IntegerField(_l("Disponibles"), default=1, 
    validators=[MinValueValidator(0)])

    
    # Estadísticas.

    count_search = models.IntegerField(_l("Búsquedas"), default=0, 
    editable=False)

    count_views = models.IntegerField(_l("Vistas"), default=0, editable=False)

    count_taken = models.IntegerField(_l("Añadidas a la cesta"), default=0,
    editable=False)

    count_sold = models.IntegerField(_l("Ventas"), default=0, editable=False)


    tags = models.CharField(max_length=700, blank=True, editable=False)



    class Meta:
        verbose_name = _("Artículo")
        verbose_name_plural = _("Artículos")
        ordering = ["-is_featured", "-available"]


    def __str__(self):
        return self.name

    def clean(self):
        self.codename = " ".join(self.codename.split()).upper()
        self.name = " ".join(self.name.split()).upper()
        self.description = " ".join(self.description.split())

        self.tags = text.Text.GetTags(self.codename, self.name, 
            self.description, combinate=True)


    def GetImg(self):
        field = self.GetFirstImageField()
        
        if field:
            return field.url
        
        return self.IMG_DEFAULT

    def GetFirstImageField(self):
        return (self.image1 or self.image2 or self.image3)

