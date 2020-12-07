import datetime

from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.utils.text import slugify
from django.urls import reverse_lazy
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

    group = models.ManyToManyField("store.Group", verbose_name=_l("Grupo"), 
    blank=True, null=True, help_text=_l("Categoría a la que pertenece."))

    brand = models.ForeignKey("store.Brand", verbose_name=_l("Marca"), 
    blank=True, null=True, on_delete=models.CASCADE,
    help_text=_l("Marca a la que pertenece."))

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

    capacity = models.DecimalField(_("Capacidad"), max_digits=17, 
    decimal_places=2, null=True, blank=True)

    capacity_type = models.CharField(_l("Capacidad (tipo)"), max_length=50,
    blank=True, help_text=_l("El tipo de medida para la capacidad indicada "
    "(ejemplos BTU, Watts, Voltios, Amperaje, Hz, etc."))

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


    slug = models.SlugField(unique=False, blank=True, null=True)

    tags = models.CharField(max_length=700, blank=True, editable=False)



    class Meta:
        verbose_name = _("Artículo")
        verbose_name_plural = _("Artículos")
        ordering = ["-is_featured", "-available"]


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("store-item-detail", kwargs={"slug": self.slug})

    def clean(self):
        self.codename = " ".join(self.codename.split()).upper()
        self.name = " ".join(self.name.split()).upper()
        self.description = " ".join(self.description.split())

        self.slug = slugify(self.name)

        self.tags = text.Text.GetTags(self.codename, self.name, 
            self.description, combinate=True)

    def GetImg(self):
        field = self.GetFirstImageField()
        
        if field:
            return field.url
        
        return self.IMG_DEFAULT

    def GetFirstImageField(self):
        return (self.image1 or self.image2 or self.image3)





class Group(models.Model):
    """
    Grupo de artículos.
    
    """
    IMG_DEFAULT = "/static/img/base/articulo.svg"

    name = models.CharField(_l("Nombre"), max_length=100, unique=True)

    description = models.CharField(_l("Descripción"), max_length=500, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="store/group/", blank=True,
    null=True)


    class Meta:
        verbose_name = _("Grupo")
        verbose_name_plural = _("Grupos")
        ordering = ["name"]

    
    def __str__(self):
        return self.name

    def clean(self):
        self.name = " ".join(self.name.split()).upper()

    def GetImg(self):
        if self.image:
            return self.image.url
        return self.IMG_DEFAULT




class Brand(models.Model):
    """
    Marcas de artículos.
    
    """
    IMG_DEFAULT = "/static/img/base/info.svg"

    name = models.CharField(_l("Nombre"), max_length=100, unique=True)

    description = models.CharField(_l("Descripción"), max_length=500, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="store/brand/", blank=True,
    null=True)


    class Meta:
        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")
        ordering = ["name"]

    
    def __str__(self):
        return self.name

    def clean(self):
        self.name = " ".join(self.name.split()).upper()

    def GetImg(self):
        if self.image:
            return self.image.url
        return self.IMG_DEFAULT