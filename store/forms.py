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