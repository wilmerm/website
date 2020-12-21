"""Integrate with admin module."""

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from .models import User






@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    search_fields = ('email__istartswith', 'first_name__istartswith', 
        'last_name__istartswith')

    list_display = ('get_image', 'get_text', 
    'is_superuser', 'is_staff')

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'initial_password', 'google_userid', 'image_url'),
        }),
        ('Información personal', {
            'fields': ('email', 'first_name', 'last_name', 'phone1', 'phone2', 
                'address'),
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    readonly_fields = ('google_userid', 'username', 'initial_password', 
        'image_url', 'email', 'first_name', 'last_name', 'phone1', 'phone2', 
        'address', 'last_login', 'date_joined')

    ordering = ('email',)

    def get_image(self, obj):
        return format_html(
            "<img src='{}' style='width: 64px; height: auto'>", obj.GetImg())

    def get_text(self, obj):
        return format_html("<b>{}</b><br>{}", obj, obj.get_full_name())

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return User.objects.none()
        return User.objects.all()



