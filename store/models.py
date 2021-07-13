import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import (ValidationError)
from django.core.validators import (MinValueValidator, MaxValueValidator)

from colorfield.fields import ColorField

from fuente import text



class Item(models.Model):
    """
    Artículo.
    """

    IMG_DEFAULT = "/static/img/base/articulo.svg"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,
    blank=True, null=True)

    codename = models.CharField(_l("Referencia"), max_length=30)

    name = models.CharField(_l("Nombre"), max_length=50)

    description = models.CharField(_l("Descripción"), max_length=700,
    blank=True)

    group = models.ManyToManyField("store.Group", verbose_name=_l("Grupo"),
    blank=True, help_text=_l("Categoría a la que pertenece."))

    brand = models.ForeignKey("store.Brand", verbose_name=_l("Marca"),
    blank=True, null=True, on_delete=models.CASCADE,
    help_text=_l("Marca a la que pertenece."))

    image_url = models.URLField(_l("URL de la imagen"), blank=True)

    image1 = models.ImageField(_l("Imagen 1"), upload_to="store/item/",
    blank=True)

    image2 = models.ImageField(_l("Imagen 2"), upload_to="store/item/",
    blank=True)

    image3 = models.ImageField(_l("Imagen 3"), upload_to="store/item/",
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

    # Contabilidad.

    pay_tax = models.BooleanField(_("Paga impuesto"), default=True)

    # Estadísticas.

    count_search = models.IntegerField(_l("Búsquedas"), default=0,
    editable=False)

    count_views = models.IntegerField(_l("Vistas"), default=0, editable=False)

    count_taken = models.IntegerField(_l("Añadidas a la cesta"), default=0,
    editable=False)

    count_sold = models.IntegerField(_l("Ventas"), default=0, editable=False)

    slug = models.SlugField(unique=False, blank=True, null=True)

    tags = models.CharField(max_length=700, blank=True, editable=False)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("artículo")
        verbose_name_plural = _l("artículos")
        ordering = ["-is_featured", "-available"]
        constraints = [
            models.UniqueConstraint(fields=["site", "codename"],
            name='unique_item'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Importante que la url esté conformada por el pk, ya que el slug lo
        # hemos establecido no único debido a que dos sites diferentes pueden
        # concidir con el mismo slug.
        return reverse_lazy("store-item-detail",
            kwargs={"pk": self.pk, "slug": self.slug})

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

        self.codename = " ".join(self.codename.split()).upper()
        self.name = " ".join(self.name.split()).upper()
        self.description = " ".join(self.description.split())

        if Item.objects.filter(
            site=self.site, codename=self.codename).exclude(pk=self.pk):
            raise ValidationError(_("Ya existe un artículo con esta referencia."))

        self.slug = slugify(self.name)

        self.tags = text.Text.GetTags(self.codename, self.name,
            self.description, combinate=True)

    def GetImg(self):
        if self.image_url:
            return self.image_url

        field = self.GetFirstImageField()

        if field:
            return field.url
        return self.IMG_DEFAULT

    def GetFirstImageField(self):
        return (self.image1 or self.image2 or self.image3)

    def CalculateAmount(self, quantity=1, price=None, tax=None,
        tax_included=True, parse=None, rounded=None):
        """
        Calcula el importe según la cantidad, precio e impuesto indicado.

        Parameters:
            quantity (int): Cantidad de artículos.

            price (Decimal): Precio (default self.price).

            tax (int or float or Decimal): Impuesto a calcular
            (default StoreSetting.objects.last().tax).

        """
        quantity = quantity or 1
        price = price or self.price
        tax_included = bool(tax_included)

        try:
            tax = tax or StoreSetting.objects.last().tax
        except (AttributeError):
            tax = None

        amount = price * quantity
        tax_amount = 0
        total = 0

        if tax:
            if tax_included:
                tax_amount = amount - (amount / ((tax / 100) + 1))
                amount = amount - tax_amount
            else:
                tax_amount = (amount * ((tax / 100) + 1)) - amount

        total = amount + tax_amount

        if parse:
            amount = parse(amount)
            tax_amount = parse(tax_amount)
            total = parse(total)

        if rounded:
            amount = round(amount, 2)
            tax_amount = round(tax_amount, 2)
            total = round(total, 2)
        return (amount, tax_amount, total)


class Group(models.Model):
    """
    Grupo de artículos.
    """
    IMG_DEFAULT = "/static/img/base/articulo.svg"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,
    blank=True, null=True)

    name = models.CharField(_l("Nombre"), max_length=100)

    description = models.CharField(_l("Descripción"), max_length=500, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="store/group/", blank=True,
    null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("Grupo")
        verbose_name_plural = _l("Grupos")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["site", "name"], name="unique_group")
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

        self.name = " ".join(self.name.split()).upper()

        if Group.objects.filter(
            site=self.site, name=self.name).exclude(pk=self.pk):
            raise ValidationError(_("Ya existe un grupo con este nombre."))

    def GetImg(self):
        if self.image:
            return self.image.url
        return self.IMG_DEFAULT


class Brand(models.Model):
    """
    Marcas de artículos.
    """
    IMG_DEFAULT = "/static/img/base/info.svg"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,
    blank=True, null=True)

    name = models.CharField(_l("Nombre"), max_length=100)

    description = models.CharField(_l("Descripción"), max_length=500, blank=True)

    image = models.ImageField(_l("Imágen"), upload_to="store/brand/", blank=True,
    null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("Marca")
        verbose_name_plural = _l("Marcas")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["site", "name"], name="unique_brand")
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

        self.name = " ".join(self.name.split()).upper()

        if Brand.objects.filter(
            site=self.site, name=self.name).exclude(pk=self.pk):
            raise ValidationError(_("Ya existe una marca con este nombre."))

    def GetImg(self):
        if self.image:
            return self.image.url
        return self.IMG_DEFAULT


class Order(models.Model):
    """
    Orden de compra.
    """
    PROCESS = "PROCESS"
    COMPLETE = "COMPLETE"
    STATUS_CHOICES = (
        (PROCESS, _("En proceso")),
        (COMPLETE, _("Completado")),
    )

    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    OTHER = "OTHER"
    PAYMENT_METHOD_CHOICES = (
        (CASH, _("Efectivo")),
        (CREDIT_CARD, _("Tarjeta de crédito")),
        (BANK_ACCOUNT, _("Cuenta de banco")),
        (OTHER, _("Otro")),
    )

    site = models.ForeignKey(Site, on_delete=models.CASCADE, editable=False,
    blank=True, null=True)

    number = models.CharField(_l("Número"), max_length=20, blank=True)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, blank=True,
    null=True)

    note = models.CharField(_l("Comentario"), max_length=700, blank=True)

    address = models.CharField(_l("Dirección"), max_length=700, blank=True)

    phone = models.CharField(_l("Teléfonos"), max_length=30, blank=True)

    payment_method = models.CharField(_l("Forma de pago"), max_length=20,
    choices=PAYMENT_METHOD_CHOICES, default=CASH)

    create_date = models.DateTimeField(_("Creación"), auto_now_add=True,
    editable=False)

    create_user = models.ForeignKey("user.User",
    verbose_name=_l("Usuario creó"), on_delete=models.SET_NULL, null=True,
    blank=True, editable=False, related_name="order_create_user")

    update_date = models.DateTimeField(_("Modificación"), auto_now=True,
    editable=False)

    update_user = models.ForeignKey("user.User",
    verbose_name=_l("Usuario modificó"), on_delete=models.SET_NULL, null=True,
    blank=True, editable=False, related_name="order_update_user")

    status = models.CharField(_l("Estado"), max_length=20, blank=True,
    choices=STATUS_CHOICES, default=PROCESS)

    status_date = models.DateTimeField(_l("Fecha del último estado"),
    blank=True, null=True)

    accepted_policies = models.BooleanField(default=False,
    verbose_name=_l("Estoy de acuerdo con las políticas del sitio"),
    help_text=_("Al marcar esta casilla usted acepta y está de acuerdo con "
    "las políticas del sitio para compras en línea."))

    # Campos de consultas que serán actualizados cada vez que se guarde un
    # movimiento de esta orden.

    amount = models.DecimalField(_l("Importe"), max_digits=17, decimal_places=2,
    blank=True, null=True)

    tax = models.DecimalField(_l("Impuestos"), max_digits=17, decimal_places=2,
    blank=True, null=True)

    total = models.DecimalField(_l("Total"), max_digits=17, decimal_places=2,
    blank=True, null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("Orden")
        verbose_name_plural = _l("Ordenes")
        constraints = [
            models.UniqueConstraint(fields=["site", "number"], name="unique_order")
        ]

    def __str__(self):
        return f"{self._meta.verbose_name} {self.number}"

    def get_absolute_url(self):
        return reverse_lazy("store-order-detail", kwargs={"pk": self.pk})

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()

            try:
                self.user = self.user or self.create_user
            except (Order.user.RelatedObjectDoesNotExist):
                self.user = self.create_user

            # siteid + today + count
            number = "%s%s%s" % (self.site.id,
                timezone.now().strftime("%Y%m%d%H%M%S"),
                Order.objects.count())
            self.number = number[:20]
        else:
            this = Order.objects.get(pk=self.pk)
            if this.status != self.status:
                self.status_date = timezone.now()

    def save(self, *args, **kwargs):
        try:
            kwargs.pop("no_update_fields")
        except (KeyError):
            self.update_all()

        return super().save(*args, **kwargs)

    def get_movs(self):
        """Obtiene los movimientos de esta orden."""
        return Mov.objects.filter(order=self)

    def update_amount(self, queryset=None):
        """Actualiza el campo 'amount' y retorna su valor."""
        queryset = queryset or self.get_movs()
        self.amount = queryset.aggregate(models.Sum("amount"))["amount__sum"] or 0
        return self.amount

    def update_tax(self, queryset=None):
        """Actualiza el campo 'tax' y retorna su valor."""
        queryset = queryset or self.get_movs()
        self.tax = queryset.aggregate(models.Sum("tax"))["tax__sum"] or 0
        return self.tax

    def update_total(self, queryset):
        """Actualiza el campo 'total' y retorna su valor."""
        queryset = queryset or self.get_movs()
        self.total = queryset.aggregate(models.Sum("total"))["total__sum"] or 0
        return self.total

    def update_all(self, queryset=None):
        """
        Actualiza todas los campos actualizables, y retorna un diccionario con
        sus valores.
        """
        queryset = queryset or self.get_movs()
        return {
            "amount": self.update_amount(queryset),
            "tax": self.update_tax(queryset),
            "total": self.update_total(queryset),
        }


class OrderNote(models.Model):
    """
    Notas y comentarios de ordenes.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    title = models.CharField(_l("Título"), max_length=100)

    content = models.CharField(_l("Contenido"), max_length=700)

    create_date = models.DateTimeField(_("Creación"), auto_now_add=True,
    editable=False)

    create_user = models.ForeignKey("user.User",
    verbose_name=_l("Usuario creó"), on_delete=models.SET_NULL, null=True,
    blank=True, editable=False, related_name="ordernote_create_user")

    class Meta:
        verbose_name = _l("Nota de orden")
        verbose_name_plural = _l("Notas de ordenes")

    def __str__(self):
        return f"{self.order}: {self.title}"


class Mov(models.Model):
    """
    Movimiento de inventario.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    cant = models.IntegerField(_l("Cantidad"))

    price = models.DecimalField(_l("Precio"), max_digits=17, decimal_places=2)

    tax = models.DecimalField(_l("Impuestos"), max_digits=17, decimal_places=2,
    default=0)

    amount = models.DecimalField(_l("Importe"), max_digits=17, decimal_places=2,
    default=0, blank=True)

    total = models.DecimalField(_l("Importe"), max_digits=17, decimal_places=2,
    default=0, blank=True)

    create_date = models.DateTimeField(_l("Creación"), auto_now_add=True,
    editable=False)

    create_user = models.ForeignKey("user.User",
    verbose_name=_l("Usuario creó"), on_delete=models.SET_NULL, null=True,
    blank=True, editable=False, related_name="mov_create_user")

    update_date = models.DateTimeField(_l("Modificación"), auto_now=True,
    editable=False)

    update_user = models.ForeignKey("user.User",
    verbose_name=_l("Usuario modificó"), on_delete=models.SET_NULL, null=True,
    blank=True, editable=False, related_name="mov_update_user")

    class Meta:
        verbose_name = _l("Movimiento")
        verbose_name_plural = _l("Movimientos")

    def __str__(self):
        return f"{self.order}: {self.item}"

    def clean(self):
        if self.item.pay_tax:
            self.amount, self.tax, self.total = self.item.CalculateAmount(
                self.cant, self.price)
        else:
            self.amount = self.price * self.cant
            self.total = self.amount


class StoreSetting(models.Model):
    """
    Configuración de la tienda.
    """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, editable=False,
    blank=True, null=True)

    tax = models.DecimalField(_l("impuesto porcentaje"), decimal_places=2,
    max_digits=5, default=18,
    help_text=_l("porcentaje de impuesto a cargar a los artículos."))

    currency_symbol = models.CharField(_l("moneda"), max_length=5, blank=True,
    help_text=_l("símbolo de la moneda en que están los precios de los items."))

    show_items_without_price = models.BooleanField(_l("mostrar artículos in precio"),
    default=False, help_text=_l("muestra los artículos aunque no tengan precio."))

    policies = models.CharField(_l("políticas de la tienda en línea"),
    max_length=700, blank=True, help_text=_l("texto que contine una versión "
    "corta de las políticas, términos y condiciones de al compara a través de "
    "la tienda en línea. Este texto aparecerá en las ordenes impresas que "
    "realicen los clientes a través la tienda en línea."))

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _l("configuración de tienda")
        verbose_name_plural = _l("configuración de tienda")

    def __str__(self):
        return str(self._meta.verbose_name)

    def clean(self):
        if not self.pk:
            self.site = Site.objects.get_current()
            # Solo puede existir una configuración por site.
            if StoreSetting.on_site.all():
                raise ValidationError(_("Ya existe una configuración de artículos."))

    @classmethod
    def get_current(self):
        """Obtiene la configuración para el sitio actual, o crea una."""
        setting = StoreSetting.on_site.last()
        if not getattr(setting, "pk", False):
            setting = StoreSetting.objects.create(site=Site.objects.get_current())
        return setting