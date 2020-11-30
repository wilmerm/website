from django.shortcuts import render
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