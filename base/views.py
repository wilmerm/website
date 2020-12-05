from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)



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
    """
    View para recibir mensajes desde la página de contacto.
    """
    name = request.GET.get("name")
    phone = request.GET.get("phone")
    email = request.GET.get("email")
    message = request.GET.get("message")

    messages.info(request, "¡Su mensaje a sido recibido! Estaremos en contacto "
    "con usted lo más pronto posible.")

    return redirect(reverse_lazy("index"))