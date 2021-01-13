from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (ListView, CreateView, UpdateView, 
    DetailView, DeleteView, TemplateView, FormView)


from fuente import (var, utils, text)

from .models import Item, Brand, Group, Order, Mov
from .forms import ItemSearchForm, ItemCartForm, OrderForm




# Método que obtiene el sitio actual.
get_current_site = Site.objects.get_current




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

        # Se muestran solo los artículos del site actual.
        qs = self.model.objects.filter(site=get_current_site(), is_active=True)

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
        context["form_cart"] = ItemCartForm(item=self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        # El artículo debe pertenecer al site actual.
        if self.get_object().site != get_current_site():
            return HttpResponseRedirect(reverse_lazy("store-item-list"))
        return super().dispatch(request, *args, **kwargs)




class OrderCreateView(LoginRequiredMixin, CreateView):
    """
    Crea una orden de compra a partir de los datos almacenados en el carrito de 
    la sesión actual: request.session['cart'] y request.session['cart_total']
    """
    model = Order
    form_class = OrderForm

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("cart"):
            return HttpResponseRedirect(reverse_lazy("store-cart"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        form.instance.user = self.request.user

        # Eliminamos el carrito de la sesión.
        self.request.session["cart"] = {}
        self.request.session["cart_total"] = {}

        messages.success(self.request, 
            _("¡Su orden ha sido creada satisfactoriamente!"))
        return super().form_valid(form)






class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Detalle de una orden del usuario actual.
    """
    model = Order

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)





class OrderListView(LoginRequiredMixin, ListView):
    """
    Listado de ordenes del usuario actual.
    """
    model = Order
    paginate_by = 20

    @utils.context_decorator()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Order.on_site.filter(user=self.request.user)
    



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





def cart_remove(request) -> JsonResponse:
    """
    Vista que quita un item del carrito.

    El carrito es almacenado como un diccionario en request.session['cart'].
    Y los totales en request.session['cart_total'].

    El parámetro url 'item_id' se usará para identificar la clave del 
    diccionario request.session.cart que corresponde al artículo a eliminar.
    Si se especifica 'all' como valor del parámetro item_id, entonces se 
    eliminarán todos los artículos del carrito.

    """
    item_id = request.GET.get("item_id")
    cart = request.session.get("cart")

    if not cart:
        return JsonResponse({"error": True, 
        "message": _("No hay artículos en el carrito.")})

    if not item_id:
        return JsonResponse({"error": True, 
        "message": _("No se encontró el artículo que intentó eliminar.")})
    elif item_id == "all":
        cart = dict()
    else:
        try:
            cart.pop(item_id)
        except (KeyError) as e:
            print(e)

    request.session["cart"] = cart
    cart_total = calculate_totals(cart)
    request.session["cart_total"] = cart_total

    return JsonResponse({"error": False, "cart": cart, "cart_total": cart_total,
    "message": _("¡Artículo removido del carrito!")})




def cart_add(request, item_id=None, cant=None, update=False) -> JsonResponse:
    """
    Vista que agrega un item al carrito, o suma la cantidad a uno ya agregado.

    El carrito es almacenado como un diccionario en request.session['cart'].
    Y los totales en request.session['cart_total'].
    
    """
    item_id = request.POST.get("item_id") or item_id
    cant = request.POST.get("cant") or cant
    update = bool(update)

    try:
        item = Item.objects.get(id=int(item_id))
    except (ObjectDoesNotExist, TypeError):
        print(item_id)
        return JsonResponse({"error": True, "message": _("No se encontró el "
        "artículo. Por favor, inténtelo nuevamente.")})

    try:
        cant = abs(int(cant))
    except (ValueError):
        cant = 1

    if not item.price:
        return JsonResponse({"error": True, "message": _("Lo sentimos, pero "
        "este artículo aun no está disponible para la venta online.")})

    price = abs(float(item.price))
    amount, tax, total = item.CalculateAmount(cant, parse=float, rounded=2)

    try:
        cart = request.session["cart"]
    except (KeyError):
        cart = {item_id: {
            "item_id": item.id, 
            "name": str(item),
            "img": item.GetImg(),
            "url": str(item.get_absolute_url()),
            "cant": cant,
            "price": price,
            "amount": amount,
            "tax": tax,
            "total": total,
            "add_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "add_username": request.user.username, 
        }}
        request.session["cart"] = cart

    if not cart.get(item_id):
        cart[item_id] = {
            "item_id": item.id, 
            "name": str(item),
            "img": item.GetImg(),
            "url": str(item.get_absolute_url()),
            "cant": cant,
            "price": price,
            "amount": amount,
            "tax": tax,
            "total": total,
            "add_date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            "add_username": request.user.username, 
            "update_date": None,
            "update_user": None,
        }
    else:
        if update is False:
            cant = cart[item_id]["cant"] + cant
        amount, tax, total = item.CalculateAmount(cant, parse=float, rounded=2)
        cart[item_id]["item_id"] = item.id
        cart[item_id]["name"] = str(item)
        cart[item_id]["img"] = item.GetImg()
        cart[item_id]["url"] = str(item.get_absolute_url())
        cart[item_id]["cant"] = cant
        cart[item_id]["price"] = price
        cart[item_id]["amount"] = amount
        cart[item_id]["tax"] = tax
        cart[item_id]["total"] = total
        cart[item_id]["update_date"] = timezone.now().strftime("%Y-%m-%d %H:%M")
        cart[item_id]["update_user"] = request.user.username
    
    request.session["cart"] = cart
    cart_total = calculate_totals(cart)
    request.session["cart_total"] = cart_total

    return JsonResponse({"error": False, "cart": cart, "cart_total": cart_total,
    "message": _("¡Artículo añadido al carrito!")})




def cart_update(request):
    """
    Actualiza el item indicado con la nueva cantidad.
    
    """
    item_id = request.GET.get("item_id")
    cant = request.GET.get("cant")
    return cart_add(request, item_id, cant, update=True)





def cart_get(request):
    """
    Obtiene el carrito de la sesión actual.
    
    """
    cart = request.session.get("cart") or {}
    cart_total = calculate_totals(cart)
    return JsonResponse({"cart": cart, "cart_total": cart_total, "error": False,
    "message": ""})




def update_from_unolet(request):
    """Actualiza los artículos desde la app Unolet configurada para el cliente."""
    import datetime
    import urllib
    import json
    import requests
    from django.conf import settings 

    domain = settings.UNOLET_APP_DOMAIN
    today = datetime.datetime.today()

    token_key = f"gszD35F{today.year-today.month-today.day-4377299}dldh-gaASDPp{today.day-today.month}-_s931_d{today.year-438844+today.day}-dsyDQe"
    token_value = f"gas-_alhhdiey7493pKSHDFASF{today.year-today.month-today.day-4377532299}dpERQE{today.day-today.month-5544543}-_s93EWERewwWfdER1_d{today.year-4566667765554+today.day}-dsWERWTgfu45TTEWyDQe"
    url = f"http://{domain}/articulo/json/articulo/list/forupdatewebsitewithunolet/?q=''&{token_key}={token_value}"


    updating = request.session.get("store_updating_from_unolet") or False

    if updating:
        return JsonResponse({"message": _("Se están actualizando los artículos. Por favor, espere...")})
    else:
        request.session["store_updating_from_unolet"] = True

    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())

    count = 0
    errors = 0
    site = Site.objects.get_current()

    for dic in data["data"]:
        
        try:
            item = Item.objects.get(codename=dic["codename"], site=site)
        except (Item.DoesNotExist):
            item = Item()
            item.codename = dic["codename"]
            item.site = site

        item.name = dic["description"]
        try:
            item.price = dic["precio"]
        except (ValueError, TypeError):
            item.price = 0
        try:
            item.available = float(dic["disponible"])
        except (ValueError, TypeError):
            item.available = 0

        try:
            item.save()
        except (BaseException) as e:
            print("Error en update_from_unolet", e, url)
            errors += 1
        else:
            count += 1

    request.session["store_updating_from_unolet"] = False
    return JsonResponse({"message": f"Se actualizaron {count} artículos. {errors} errores."})

    
   



# ------------------------------------------------------------------------------
# Funciones que no son vistas.
# ------------------------------------------------------------------------------

def calculate_totals(cart: dict) -> dict:
    """
    Calcula los totales del carrito de compra indicado.
    
    """
    cant = 0 # Cantidad de items.
    subtotal = 0
    tax = 0
    total = 0

    for key in cart:
        cant += int(cart[key]["cant"])
        subtotal += float(cart[key]["amount"])
        tax += float(cart[key]["tax"])
        total += float(cart[key]["total"])
        
    return {
        "cant": cant, 
        "count": len(cart),
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }