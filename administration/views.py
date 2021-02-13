import datetime

from django.shortcuts import render, redirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)
from base.models import VisitCounter, Message



class StaffRequiredMixin():
    """Valida que el usuario sea staff o superuser, o lanza un Http404 error."""
    def dispatch(self, request, *args, **kwargs):
        if (not request.user.is_staff) and (not request.user.is_superuser):
            raise Http404("Permiso denegado.")
        return super().dispatch(request, *args, **kwargs)


class IndexView(StaffRequiredMixin, TemplateView):
    """Página principal del panel de administración."""
    template_name = "administration/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessageUpdateView(StaffRequiredMixin, UpdateView):
    """Página de administración de mensajes recibidos."""
    template_name = "administration/message.html"
    model = Message
    fields = ["read_note"]

    def form_valid(self, form):
        if not form.instance.read_date:
            form.instance.read_date = timezone.now()
            form.instance.read_user = self.request.user
        return super().form_valid(form)
