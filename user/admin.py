"""Integrate with admin module."""

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Profile




@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email__istartswith', 'first_name__istartswith', 
        'last_name__istartswith')
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 
        'is_staff')
    ordering = ('email',)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return User.objects.none()
        return User.objects.all()




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Perfil de usuario.

    """
    search_fields = ('user__email__istartswith', 'user__first_name__istartswith', 
        'user__last_name__istartswith')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"].widget = forms.Textarea()
        return form

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('__str__', 'site', 'get_first_name', 'get_last_name', 
            'get_is_superuser', 'get_is_staff', 'is_active')
        return ('__str__', 'is_active')

    def get_user(self, obj):
        return obj.user

    def get_email(self, obj):
        return self.get_user(obj).email
    
    def get_first_name(self, obj):
        return self.get_user(obj).first_name
    
    def get_last_name(self, obj):
        return self.get_user(obj).last_name

    def get_full_name(self, obj):
        return self.get_user(obj).get_full_name()

    def get_is_superuser(self, obj):
        return self.get_user(obj).is_superuser

    def get_is_staff(self, obj):
        return self.get_user(obj).is_staff

    