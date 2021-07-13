from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.db import models
from django.utils.translation import gettext as _

from .models import Item, Group, Brand, Order, OrderNote, Mov, StoreSetting




get_current_site = Site.objects.get_current



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": ("codename", "name", "description", "group", "brand",
                        "price", "is_active", "is_featured", "available")
        }),
        (_("Imagen"), {
            "fields": ("image_url", "image1", "image2", "image3"),
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

    search_fields = ("codename__istartswith", "name__icontains",
    "brand__name__istartswith")

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("get_image", "get_text", "brand", "price", "available",
                "is_featured", "is_active", "count_views", "count_taken",
                "count_sold", "site")
        return ("get_image", "get_text", "brand", "price", "available",
            "is_featured", "is_active", "count_views", "count_taken",
            "count_sold")


    def get_queryset(self, request):
        if request.user.is_superuser:
            return Item.objects.all()
        return Item.objects.filter(site=get_current_site())

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["description"].widget = forms.Textarea()
        form.base_fields["group"].queryset = Group.objects.filter(site=get_current_site())
        form.base_fields["brand"].queryset = Brand.objects.filter(site=get_current_site())
        return form

    def get_image(self, obj):
        return format_html("<img src='{}' style='width: auto; height: 64px'>",
        obj.GetImg())

    def get_text(self, obj):
        return format_html("<p><b>{}</b>: {}<br>{}</p>", obj.codename, obj.name, obj.description)




@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("get_image", "name", "description", "site")
        return ("get_image", "name", "description")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Group.objects.all()
        return Group.objects.filter(site=get_current_site())

    def get_image(self, obj):
        return format_html("<img src='{}' style='width: auto; height: 64px'>",
        obj.GetImg())




@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("get_image", "name", "description", "site")
        return ("get_image", "name", "description")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Brand.objects.all()
        return Brand.objects.filter(site=get_current_site())

    def get_image(self, obj):
        return format_html("<img src='{}' style='width: auto; height: 64px'>",
        obj.GetImg())




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ("number",)
    readonly_fields = ("create_date", "create_user", "update_date", "update_user")

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("number", "user", "create_date", "payment_method",
                "status", "site")
        return ("number", "user", "create_date", "payment_method", "status")

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ("site", "user", "payment_method", "create_date", "status",
                "accepted_policies")
        return ("user", "payment_method", "create_date", "status")


    def get_queryset(self, request):
        if request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(site=get_current_site())




@admin.register(OrderNote)
class OrderNoteAdmin(admin.ModelAdmin):
    search_fields = ("order__number",)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "get_site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return OrderNote.objects.all()
        return OrderNote.objects.filter(order__site=get_current_site())

    def get_site(self, obj):
        return obj.order.site




@admin.register(Mov)
class MovAdmin(admin.ModelAdmin):
    search_fields = ("order__number",)
    readonly_fields = ("amount", "total", "create_date", "create_user",
        "update_date", "update_user")

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("order", "item", "cant", "price", "tax", "amount", "total", "get_site")
        return ("order", "item", "cant", "price", "tax", "amount", "total")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Mov.objects.all()
        return Mov.objects.filter(order__site=get_current_site())

    def get_site(self, obj):
        return obj.order.site



@admin.register(StoreSetting)
class StoreSettingAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return StoreSetting.objects.all()
        return StoreSetting.objects.filter(site=get_current_site())

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["policies"].widget = forms.Textarea()
        return form


