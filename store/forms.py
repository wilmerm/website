from django import forms
from django.utils.translation import gettext as _

#from dal import autocomplete

from .models import Item, Brand, Group





class ItemSearchForm(forms.Form):
    """
    Formulario de búsqueda de artículos.
    
    """
    q = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={"type": "search", "placeholder": _('Buscar...')}))
    
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), 
    empty_label=_("Todas las marcas"), label=_("Marca"), required=False)

    group = forms.ModelChoiceField(queryset=Group.objects.all(), 
    empty_label=_("Todas los grupos"), label=_("Grupo"), required=False)





class ItemCartForm(forms.Form):
    """
    Añade un nuevo artículo al carrito.
    El carrito es almacenado en las sessión actual.
    """

    item_id = forms.IntegerField()
    cant = forms.IntegerField(min_value=1, label=_("Cantidad"))

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop("item")
        super().__init__(*args, **kwargs)

        self.fields["cant"].initial = 1
        self.fields["cant"].widget.attrs.update(
            {"class": "form-control-lg font-size-large w-256px text-right"})

        self.fields["item_id"].value = self.item.id