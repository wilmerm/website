from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django import forms

from tinymce.widgets import TinyMCE

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide, 
Schedule, BrandRepresented, Question, SampleImage, SampleVideo, VisitCounter)




get_current_site = Site.objects.get_current



@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    search_fields = ("website_name__icontains",)

    fieldsets = (
        (None, {
            'fields': ('website_name', 'description', 'logo', 'icon'),
        }),
        (_('Contactos'), {
            'fields': (('phone1', 'phone2'), ('email', 'schedule'), 'address'),
        }),
        (_('Acerca de'), {
            'fields': ('about_title', 'about_content', 'about_image_cover', 
                'about_image_footer'),
        }),
        (_('Información'), {
            'fields': ('information_title', 'information_content'),
        }),
        (_('Mensaje de nuevos registros'), {
            'fields': ('registration_message',),
        }),
        (_('Contenido externo'), {
            'fields': ('embed_map_html', 'embed_promo_url'),
        }),
    )

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Setting.objects.all()
        return Setting.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['description'].widget = forms.Textarea(
            attrs={'rows': 3})
        form.base_fields['about_title'].widget = TinyMCE(
            mce_attrs={'height': 128})
        form.base_fields['about_content'].widget = TinyMCE()
        form.base_fields['information_title'].widget = TinyMCE(
            mce_attrs={'height': 128, 'forced_root_block': 'false'})
        form.base_fields['information_content'].widget = TinyMCE()
        form.base_fields['registration_message'].widget = TinyMCE()
        return form




@admin.register(AdvancedSetting)
class AdvancedSettingAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return AdvancedSetting.objects.all()
        return AdvancedSetting.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form




@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('get_icon', '__str__', 'index', 'get_url', 'site')
    search_fields = ('social_network_name__istartswith', 'url__icontains')
    list_display_links = ('get_icon', '__str__')

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('get_icon', '__str__', 'index', 'get_url', 'site')
        return ('get_icon', '__str__', 'index', 'get_url')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return SocialNetwork.objects.all()
        return SocialNetwork.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_icon(self, obj):
        return format_html("<img src='{}' style='width: 24px; height: 24px'>",
        obj.GetImg())

    def get_url(self, obj):
        return format_html("<a href='{}' target='_blank'>{}</a>", obj.url, obj.url)




@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'get_text', 'site')
    search_fields = ('title__icontains',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('get_image', 'get_text', 'site')
        return ('get_image', 'get_text')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Slide.objects.all()
        return Slide.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['description'].widget = forms.Textarea()
        return form

    def get_image(self, obj):
        return format_html("<img src='{}' style='width: auto; height: 128px'>",
        obj.GetImg())

    def get_text(self, obj):
        return format_html("<p><b>{}</b><br>{}</p>", obj.title, obj.description)




@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Schedule.objects.all()
        return Schedule.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form




@admin.register(BrandRepresented)
class BrandRepresentedAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return BrandRepresented.objects.all()
        return BrandRepresented.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form




@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('question__icontains', 'answer__icontains')

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ("__str__", "site")
        return ("__str__",)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Question.objects.all()
        return Question.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['question'].widget.attrs.update({'style': 'width: 50%'})
        form.base_fields['answer'].widget = TinyMCE()
        return form




@admin.register(SampleImage)
class SampleImageAdmin(admin.ModelAdmin):
    search_fields = ('title__icontains',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('get_image', 'title', 'description', "site")
        return ('get_image', 'title', 'description')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return SampleImage.objects.all()
        return SampleImage.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_image(self, obj):
        return format_html("<img src='{}' style='width: 64px; height: auto'>", 
        obj.image.url)




@admin.register(SampleVideo)
class SampleVideoAdmin(admin.ModelAdmin):
    search_fields = ('title__icontains',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('title', 'description', 'site')
        return ('title', 'description')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return SampleVideo.objects.all()
        return SampleVideo.on_site.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form





@admin.register(VisitCounter)
class VisitCounterAdmin(admin.ModelAdmin):
    readonly_fields = ("site", "urlpath", "count", "date")
    list_display = ("get_url", "count", "date")
    list_filter = ("urlpath", "date")
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return VisitCounter.objects.all()
        return VisitCounter.on_site.all()

    def get_url(self, obj):
        return "%s%s" % (obj.site, obj.urlpath)
