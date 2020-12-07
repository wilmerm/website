from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView)

from fuente import (var, utils, text)

from .models import Item, Brand, Group
from .forms import ItemSearchForm





class ItemListView(ListView):
    """
    Listado de artículos.
    """
    model = Item
    paginate_by = 30

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_search"] = ItemSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        q = self.request.GET.get("q")
        brand =self.request.GET.get("brand")
        group = self.request.GET.get("group")
        qs = self.model.objects.filter(is_active=True)

        if brand:
            qs = qs.filter(brand=brand)

        if group:
            qs = qs.filter(group=group)

        if q:
            qs = qs.filter(tags__contains=text.Text.GetTag(q))

        return qs




class ItemDetailView(DetailView):
    """
    Detalle de un artículo.
    """
    model = Item

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = str(self.object)
        context["description"] = self.object.description
        context["form_search"] = ItemSearchForm(self.request.GET)
        return context