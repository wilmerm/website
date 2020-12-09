from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView, FormView)


from fuente import (var, utils, text)

from .models import Item, Brand, Group
from .forms import ItemSearchForm, ItemCartForm





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
        context["form_cart"] = ItemCartForm(self.request.POST, item=self.object)
        return context




class CartView(TemplateView):
    """
    Detalle de un artículo.
    """
    template_name = "store/cart.html"

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_search"] = ItemSearchForm(self.request.GET)
        return context





def cart_add(request):

    item_id = request.POST.get("item_id")
    cant = request.POST.get("cant")

    try:
        item = Item.objects.get(id=int(item_id))
    except (ObjectDoesNotExist, TypeError):
        return JsonResponse({"error": True, "message": _("No se encontró el "
        "artículo. Por favor, inténtelo nuevamente.")})

    try:
        cant = int(cant)
    except (ValueError):
        cant = 1

    if not item.price:
        return JsonResponse({"error": True, "message": _("Lo sentimos, pero "
        "este artículo aun no está disponible para la venta online.")})

    price = float(item.price)

    try:
        cart = request.session["cart"]
    except (KeyError):
        cart = {item_id: {
            "item_id": item.id, 
            "name": str(item),
            "img": item.GetImg(),
            "cant": cant,
            "price": price,
            "subtotal": cant * price,
            "add_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "add_username": request.user.username, 
            }}
        request.session["cart"] = cart

    if not cart.get(item_id):
        cart[item_id] = {
            "item_id": item.id, 
            "name": str(item),
            "img": item.GetImg(),
            "cant": cant,
            "price": price,
            "subtotal": cant * price,
            "add_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "add_username": request.user.username, 
            "update_date": None,
            "update_user": None,
            }
    else:
        cart[item_id]["item_id"] = item.id
        cart[item_id]["name"] = str(item)
        cart[item_id]["img"] = item.GetImg()
        cart[item_id]["cant"] += cant
        cart[item_id]["price"] = price
        cart[item_id]["subtotal"] = cant * price
        cart[item_id]["update_date"] = timezone.now().strftime("%Y-%m-%d %H:%M")
        cart[item_id]["update_user"] = request.user.username
    
    request.session["cart"] = cart

    # Calcular los totales.
    total = 0
    cant = 0
    for key in cart:
        total += cart[key]["subtotal"]
        cant += cart[key]["cant"]
    
    request.session["cart_total"] = {"cant": cant, "total": total}

    return JsonResponse({"error": False, 
    "message": _("¡Artículo añadido al carrito!")})