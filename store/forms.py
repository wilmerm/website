from decimal import Decimal
from django import forms
from django.utils.translation import gettext as _
from django.contrib.sites.models import Site

#from dal import autocomplete

from .models import Item, Brand, Group, Order, OrderNote, Mov


# Método que obtiene el site actual.
get_current_site = Site.objects.get_current




class ItemSearchForm(forms.Form):
    """
    Formulario de búsqueda de artículos.
    
    """
    q = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={"type": "search", "placeholder": _('Buscar...')}))
    
    # Queryset filtrado por el site actual.
    brand = forms.ModelChoiceField(empty_label=_("Todas las marcas"), 
    label=_("Marca"), required=False, 
    queryset=Brand.on_site.all())

    # Queryset filtrador por el site actual.
    group = forms.ModelChoiceField(empty_label=_("Todas los grupos"), 
    label=_("Grupo"), required=False, 
    queryset=Group.on_site.all())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)






class ItemCartForm(forms.Form):
    """
    Añade un nuevo artículo al carrito.
    El carrito es almacenado en las sesión actual.

    """
    item_id = forms.IntegerField(widget=forms.HiddenInput())

    cant = forms.IntegerField(min_value=1, label=_("Cantidad"))


    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop("item")
        super().__init__(*args, **kwargs)

        self.fields["cant"].initial = 1
        self.fields["cant"].widget.attrs.update(
            {"class": "form-control-lg font-size-large text-right"})

        self.fields["item_id"].value = self.item.id





class OrderForm(forms.ModelForm):
    """
    Crea o modifica una orden.
    
    """
    
    class Meta:
        model = Order
        fields = ("address", "phone", "payment_method", "note", 
            "accepted_policies")

    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

        self.user = request.user
        self.cart = request.session.get("cart")
        self.cart_total = request.session.get("cart_total")
        self.mov_list = [] # Se usará para ir poniendo los movimientos validados.

        self.fields["address"].widget = forms.Textarea(attrs={"rows": 2})
        
        self.fields["note"].widget = forms.Textarea(attrs={"rows": 2, 
            "placeholder": _("Comentario adicional (opcional).")})

        self.fields["accepted_policies"].required = True
        self.fields["address"].initial = self.user.address
        self.fields["phone"].initial = self.user.phone1
        
    def clean(self):
        cd = super().clean()
        
        # Aquí validamos y añadimos los movimientos.
        
        if not self.user:
            raise forms.ValidationError(_("Debe iniciar sessión para continuar."))

        if not self.cart:
            raise forms.ValidationError(_("No hay artículos en el carrito."))
        
        for key in self.cart:
            mov_cart = self.cart[key]
            mov = Mov()

            # Validamos el artículo.
            try:
                item = Item.on_site.get(id=int(mov_cart["item_id"]))
            except (Item.DoesNotExist):
                raise forms.ValidationError("%s %s" % (_("No está disponible el "
                    "artículo"), mov_cart["name"]))
            except (BaseException) as e:
                print(self.user, "OrderForm", e)
                raise forms.ValidationError(_("Ha ocurrido un error inesperado. "
                    "Inténtelo nuevamente y si el inconveniente persiste "
                    "comuníquese con soporte técnico."))
            mov.item = item

            # Validamos la cantidad
            try:
                mov.cant = int(mov_cart["cant"])
            except (ValueError, KeyError) as e:
                print(self.user, "OrderForm", e)
                raise forms.ValidationError(_("No es válida la cantidad en el "
                    "artículo ") + str(item))
                
            # Validamos el precio.
            try:
                mov.price = Decimal(mov_cart["price"])
            except (BaseException) as e:
                print(self.user, "OrderForm", e)
                raise forms.ValidationError(_("No es válido el precio en el "
                    "artículo ") + str(item))

            # El monto, impuesto y total se calculará en la 
            # validación del movimiento.
            try:
                mov.clean()
            except (forms.ValidationError) as e:
                raise forms.ValidationError(e)
            except (BaseException) as e:
                print(self.user, "OrderForm", e)
                raise forms.ValidationError(_("Ocurrió un error tratando de "
                "procesar el artículo ") + str(item) + " " + _("Comuníquese "
                "con soporte técnico para más detalles."))

            # La orden se agregará en el save método, y también se guardarán alli.
            self.mov_list.append(mov)

        self.cleaned_data = cd
        return self.cleaned_data

    def save(self, commit=True):
        if commit:
            # Guardamos el la orden y añadimos cada uno de sus movimientos.
            instance = super().save(commit=True)
            for mov in self.mov_list:
                mov.order = instance
                mov.save()
        return super().save(commit)
