import datetime

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)
from base.models import Message
from base.forms import MessageForm


class IndexView(TemplateView):
    """Página principal."""

    template_name = "base/index.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    """Acerca de."""

    template_name = "base/about.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandsView(TemplateView):
    """Marcas."""

    template_name = "base/brands.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CalcBTUView(TemplateView):
    """Calculadora de BTU."""

    template_name = "base/calcbtu.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class QuestionsView(TemplateView):
    """Calculadora de BTU."""

    template_name = "base/questions.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PolicyView(TemplateView):
    """Políticas."""

    template_name = "base/policy.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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

    print(request.session["message_send"])

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
    
            
