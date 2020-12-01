from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _

from .models import Item





class ItemForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(
        attrs={"style": "width: 80%"}))

    class Meta:
        model = Item
        fields = "__all__"



class ItemAdmin(admin.ModelAdmin):

    form = ItemForm
    
    fieldsets = (
        (None, {
            "fields": ("codename", "name", "description", "price", "is_active", 
            "is_featured")
        }),
        (_("Imagen"), {
            "fields": ("image1", "image2", "image3"),
        }),
        (_("Color"), {
            "fields": (("color1", "color2"),),
        }),
        (_("Otras características físicas"), {
            "fields": (
                ("weight", "weight_type"), 
                ("volumen", "volumen_type"), 
                ("length_width", "length_height", "length_depth", "length_type"), 
                "material",)
        }),
        (_("Características técnicas"), {
            "fields": (("capacity", "capacity_type"),),
            "classes": ('wide', 'extrapretty'),
            #"description": _("Estadísticas de uso para este artículo."),
        }), 
    )

    readonly_fields = ("count_search", "count_views", "count_taken", "count_sold")

    list_display = ("codename", "name", "price", "is_featured", "is_active")


admin.site.register(Item, ItemAdmin)