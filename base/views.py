import datetime
from django.http.response import JsonResponse

from django.shortcuts import render, redirect, HttpResponse
from django.urls import base, reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)
from base.models import Message, Setting, AdvancedSetting, SocialNetwork
from base.forms import MessageForm




def handler400(request, *args, **kwargs):
    return render(request, template_name="error/400.html", context={}, status=400)


def handler403(request, *args, **kwargs):
    return render(request, template_name="error/403.html", context={}, status=403)


def handler404(request, *args, **kwargs):
    return render(request, template_name="error/404.html", context={}, status=404)


def handler500(request, *args, **kwargs):
    return render(request, template_name="error/500.html", context={}, status=500)



class BaseView:
    """Clase base para todas las vistas."""

    @classmethod
    def get_setting(cls):
        return Setting.GetForCurrentSite()

    def get_context_data(self, **kwargs):
        setting = self.get_setting()
        context = super().get_context_data(**kwargs)
        context["message_form"] = MessageForm(self.request.GET)
        context["setting"] = setting
        context["title"] = setting.website_name
        context["description"] = setting.description
        context["logo"] = setting.logo
        context["author"] = "Unolet (www.unolet.com)"
        return context


class IndexView(BaseView, TemplateView):
    """Página principal."""
    template_name = "base/index.html"


class AboutView(BaseView, TemplateView):
    """Acerca de."""
    template_name = "base/about.html"


class BrandsView(BaseView, TemplateView):
    """Marcas."""
    template_name = "base/brands.html"


class CalcBTUView(BaseView, TemplateView):
    """Calculadora de BTU."""
    template_name = "base/calcbtu.html"


class CatalogueView(BaseView, TemplateView):
    """Catálogo de productos."""
    template_name = "base/catalogue.html"


class QuestionsView(BaseView, TemplateView):
    """Calculadora de BTU."""
    template_name = "base/questions.html"


class PolicyView(BaseView, TemplateView):
    """Políticas."""
    template_name = "base/policy.html"


def contact_view(request):
    """View para recibir mensajes desde la página de contacto."""
    name = request.POST.get("name") or ""
    email = request.POST.get("email") or "" # requerido o phone.
    phone = request.POST.get("phone") or "" # requerido o email.
    # address = request.GET.get("address") or ""
    # service_type = request.GET.get("service_type") or ""
    # warranty = request.GET.get("warranty") or ""
    # message = request.GET.get("message") or ""

    request.session["message_send"] = (request.session.get("message_send") or 
        {"date": None, "email": email, "phone": phone, "name": name})

    # Prevenimos que el usuario envie multiples mensajes en un mismo día.
    if request.session["message_send"]["date"] == str(datetime.date.today()):
        if ((request.session["message_send"]["email"] == email) or 
            (request.session["message_send"]["phone"] == phone)):
            messages.info(request, _("Hemos recibido su mensaje. "
                "Estaremos en contacto con usted lo más pronto posible."))
            return redirect(reverse_lazy("index"))
            
    if (not email) and (not phone):
        messages.warning(request, _("Debe indicar su correo electrónico o "
            "número de teléfono donde podamos contactarlo."))
        return redirect(reverse_lazy("index"))

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.info(request, "¡Su mensaje ha sido recibido! Estaremos en "
                "contacto con usted lo más pronto posible.")
            request.session["message_send"] = {
                "date": str(datetime.date.today()),
                "email": instance.email,
                "phone": instance.phone,
                "name": instance.name,
            }
        else:
            print(form.errors)
    return redirect(reverse_lazy("index"))
    
            
# Api.

def api_message_form(request) -> JsonResponse:
    """Guarda un mensaje enviado desde un visitante."""
    name = request.POST.get("name") or ""
    email = request.POST.get("email") or "" # requerido o phone.
    phone = request.POST.get("phone") or "" # requerido o email.
    address = request.POST.get("address") or ""
    service_type = request.POST.get("service_type") or ""
    warranty = request.POST.get("warranty") or ""
    message = request.POST.get("message") or ""

    # Prevenimos que el usuario envie multiples mensajes en un mismo día.
    request.session["message_send"] = (request.session.get("message_send") or 
        {"date": None, "email": email, "phone": phone, "name": name})

    if request.session["message_send"]["date"] == str(datetime.date.today()):
        if ((request.session["message_send"]["email"] == email) or 
            (request.session["message_send"]["phone"] == phone)):
            return JsonResponse({"error": False, "message": _("Hemos recibido "
            "su mensaje. Estaremos en contacto con usted lo más pronto posible.")})
            
    if (not email) and (not phone):
        return JsonResponse({"error": True, "message": _("Debe indicar su "
        "correo electrónico o número de teléfono donde podamos contactarlo.")})

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            instance = form.save()
            request.session["message_send"] = {
                "date": str(datetime.date.today()),
                "email": instance.email,
                "phone": instance.phone,
                "name": instance.name,
            }
            return JsonResponse({"error": False, "message": _("¡Su mensaje ha "
            "sido recibido! Estaremos en contacto con usted lo más pronto posible.")})
        return JsonResponse({"error": True, 
        "message": _("Verifique los errores."), "errors": form.errors.as_json()})