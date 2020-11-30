from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)

from .models import Item




class ItemListView(ListView):
    """Listado de artículos."""

    model = Item
    #paginate_by = 50

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        q = self.request.GET.get("q")
        qs = self.model.objects.filter(is_active=True)

        if q:
            qs = qs.filter(tags__contains=text.Text.GetTag(q))

        return qs