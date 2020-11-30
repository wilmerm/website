"""
Conjunto de utilidades.
"""

import sys
from io import BytesIO
import datetime
import itertools
from decimal import Decimal
import warnings

try:
    import barcode
    from barcode.writer import SVGWriter, ImageWriter
except (ImportError):
    pass

from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse, NoReverseMatch
import django.views.generic
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import (login_required, permission_required, user_passes_test)
from simple_history.models import HistoricalRecords

from fuente import (var, html, text, json, report)
import fuente





def valuecallable(obj):
    """
    Intenta invocar el objeto --> obj() y retorna su valor.
    """
    try:
        return obj()
    except (TypeError):
        return obj



def supergetattr(obj, name, default="", get_display_name=True):
    """
    Una función getattr con super poderes.

    Si el nombre 'name' contiene puntos (.) se asume que son varios Nombres
    uno es un método del otro en el mismo orden.

    Parameters:

        obj (object): Cualquier objeto.

        name (str):

    >> supergetattr(obj, 'a.b.c', False)
    a = obj.a() or obj.a
    b = a.b() or a.b
    c = b.c() or b.c

    >> supergetattr(obj, 'a.b')
    a = obj.a() or obj.a
    b = a.get_display_b() or a.get_display_b or a.b() or a.b

    >> supergetattr(obj, 'a')
    a = obj.get_a_display() or obj.get_a_display or obj.a() or obj.a

    """
    names = name.split(".")
    if get_display_name:
        name_end = names[-1]
        names[-1] = f"get_{names[-1]}_display"

    attr = obj
    for nam in names:
        try:
            attr = valuecallable(getattr(attr, nam))
        except (AttributeError):
            if get_display_name:
                attr = valuecallable(getattr(attr, name_end, default))
    return attr




def get_pk_from_url(url):
    """
    Obtiene el valor 'pk' de la url.
    """
    # WARNING: Obsolota.
    warnings.warn()
    parts = url.split("/")
    for part in parts:
        try:
            return int(part)
        except (TypeError, ValueError):
            continue
    return None



def get_barcode(code, strtype="code128", render=True, options=None):
    """
    Obtiene el código de barras con python-barcode.

    https://python-barcode.readthedocs.io/en/latest/
    https://pypi.org/project/python-barcode/

    Parameters:
        code (str): Código en string del barcode a obtener.

        strtype (str): 'code39', 'code128', 'ean', 'ean13', 'ean8', 'gs1',
        'gtin','isbn', 'isbn10', 'isbn13', 'issn', 'jan', 'pzn', 'upc', 'upca'

        render (bool): (default=True) le aplica el método 'render()' a la salida,
        obteniendo así el contenido en string del SVG

        options (dict): (default={compress=True}) opciones que se pasarán al render.

    Returns:
        barcode (object): barcode.get_barcode_class(strtype)(str(code)).render()
    """
    c = barcode.get_barcode_class(strtype)(str(code), writer=SVGWriter())
    if (render is True):
        opt = dict(compress=True)
        opt.update(options or {})
        return c.render(opt).decode("utf-8")
    return c



class context_decorator:
    """
    Docorador para el método get_context_data en las vistas genéricas de Django.
    """
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, func):
        def method(*args, **kwargs):
            context = func(*args, **kwargs)
            return self.get_context_data(**context)
        return method

    @classmethod
    def get_context_data(self, **context):

        view = context.get("view", None)
        view_kwargs = getattr(view, "kwargs", dict())
        model = getattr(view, "model", context.get("model"))
        model_meta = getattr(model, "_meta", None)
        request = getattr(view, "request", context.get("request"))
        pk = view_kwargs.get("pk", context.get("pk"))
        is_listview = isinstance(view, django.views.generic.ListView) or context.get("is_listview")
        try:
            base_url = context.get("base_url", request.resolver_match.url_name)
        except (AttributeError):
            base_url = None

        #view = context["view"]
        #request = view.request
        #model = getattr(view, "model", )
        #delete pk = get_pk_from_url(request.path)
        #pk = view.kwargs.get("pk")

        # subtitle.
        # ----------------------------------------------------------------------
        if (context.get("subtitle") is None):
            if (context.get("object")):
                context["subtitle"] = str(context["object"])
            elif model_meta != None:
                if is_listview:
                    context["subtitle"] = getattr(model_meta, "verbose_name_plural", "")
                else:
                    context["subtitle"] = getattr(model_meta, "verbose_name", "")

        # submenu.
        # ----------------------------------------------------------------------        
        # Menú de opciones que se mostrará en la página.
        # Botón página principal del módulo.
        mindex = html.a(inner=html.img(src=var.IMG_HOME,
        alt=_("Indice")), id="menu-index", data="index",
        cssclass="btn btn-light btn-sm", title=_("Página principal del módulo."))
        # Botón istado.
        mlist = html.a(inner=html.img(src=var.IMG_LIST,
        alt=_("Listado")), id="menu-list", data="list",
        cssclass="btn btn-light btn-sm", title=_("Ir al listado."))
        # Botón crear nuevo.
        mcreate = html.a(inner=html.img(src=var.IMG_ADD,
        alt=_("Nuevo")), id="menu-create", data="create",
        cssclass="btn btn-light btn-sm", title=_("Crear nuevo registro."))
        # Botón modificar.
        mupdate = html.a(inner=html.img(src=var.IMG_EDIT,
        alt=_("Modificar")), id="menu-update", data="update",
        cssclass="btn btn-light btn-sm", title=_("Modificar este registro."))
        # Botón eliminar.
        mdelete = html.a(inner=html.img(src=var.IMG_DELETE,
        alt=_("Eliminar")), id="menu-delete", data="delete",
        cssclass="btn btn-danger btn-sm", title=_("Eliminar este registro."))
        # Botón imprimir.
        mprint = html.a(inner=html.img(src=var.IMG_PRINT,
        alt=_("Imprimir")), id="menu-print", data="print", target="_blank",
        cssclass="btn btn-info btn-sm", title=_("Imprimir este registro."))
        # Botón imprimir alternativo, para cuando no exista una url
        # app-model-print. Este botón no tendrá url, en cambio tendrá un evento
        # onclick='window.print()'.
        mprint_alt = html.a(inner=html.img(src=var.IMG_PRINT,
        alt=_("Imprimir")), id="menu-print-alt", data="print_alt",
        onclick="window.print()", cssclass="btn btn-info btn-sm",
        title=_("Imprimir."))

        # Es posible declarar en la vista estos menús a nuestro antojo.
        mindex = context.get("mindex", mindex)
        mlist = context.get("mlist", mlist)
        mcreate = context.get("mcreate", mcreate)
        mupdate = context.get("mupdate", mupdate)
        mdelete = context.get("mdelete", mdelete)
        mprint = context.get("mprint", mprint)

        menus = [mindex, mlist, mcreate, mupdate, mdelete, mprint]

        # Si el submenú no se establece en la vista, lo establecemos aquí.
        if (not context.get("submenu")) and (not context.get("submenu_nueva_version")):
            # Tratamos de obtener el nombre de la url desde el objeto request.
            # o reconstruyendola desde el nombre del modelo y la aplicación.
            if not base_url:
                # Tratamos de obtenerla contruyendola con el modelo y la vista.
                if model_meta != None:
                    model_name = getattr(model_meta, "model_name", str(model).lower())
                    app_label = getattr(model_meta, "app_label", "")
                    base_url = f"{app_label}-{model_name}"
                else:
                    base_url = ""

            # Quitamos los nombres al final que podrian coicindir con uno de los
            # menus específicos y no necesariamente uno 'base' que es lo que queremos.
            # app-model-detail -> app-model
            mnames = ("list", "detail", "update", "create", "delete", "print")
            if (base_url.split("-")[-1].lower() in mnames):
                base_url = "-".join(base_url.split("-")[:-1])

            context["base_url"] = base_url

            submenu = list()
            menus_add = list()

            for menu in menus:
                url_name = f"{base_url}-{menu.data}"
                # Obtenemos la URL del botón mediante reverse. Primero evaluándola
                # con el argumento pk, y si falla la evaluamos sin agumentos.
                # Los botones que fallen la evaluación no serán incluidos.
                try:
                    menu.href = reverse(url_name, kwargs={"pk": pk})
                except (NoReverseMatch):
                    try:
                        menu.href = reverse(url_name)
                    except (NoReverseMatch):
                        continue

                submenu.append(menu)
                menus_add.append(str(menu.data))

            # Si el menu-print no se especifica, será agregado en su lugar el
            # menu-print_alt, que tendrá un evento onclick='window.print()'.
            if (not "print" in menus_add):
                submenu.append(mprint_alt)

            context["submenu_nueva_version"] = submenu
        return context




class Menu(object):
    """
    Crea objetos que se utilizan como menus en las plantillas HTML.

    *** DeprecationWarning ***
    """
    def __init__(self, id, name, url="", img="", selected=False, help="", targetblank=False, clase="", style=""):
        warnings.warn("fuente.utils.Menu", DeprecationWarning)
        self.id = id
        self.name = _(name)
        self.url = url
        self.img = img
        self.selected = selected
        self.help = _(help)
        self.targetblank = targetblank
        self.clase = clase
        self.style = style

        if targetblank == True:
            self.target = "_blank"
        else:
            self.target = ""

        if selected == False:
            self.cssclass = ""
        else:
            self.cssclass = "selected"

        if clase:
            self.cssclass += " {}".format(clase.strip())


    def __str__(self):
        return str(self.name)

    def Html(self):

        if self.img:
            if self.selected == False:
                return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}" target="{target}"><img src="{img}"/>{name}</a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, target=self.target, img=self.img, name=self.name)
            return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}" target="{target}"><img src="{img}"/>{name}</a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, target=self.target, img=self.img, name=self.name)
        else:
            if self.selected == False:
                return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}" target="{target}"><span>{name}</span></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, target=self.target, name=self.name)
            return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}" target="{target}"><span>{name}</span></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, target=self.target, name=self.name)


    def HtmlOnlyImg(self):
        """Lo mismo que Html() solo que en este caso
        retorna solo la imagen (si la tiene), sino el texto."""
        return f"<a class='{self.cssclass}' id='{self.id}' href='{self.url}' title='{self.name}. {self.help}' target='{self.target}'><img src='{self.img}' alt='{self.name}'></a>"


    def Selected(self, state=True):
        self.selected = state

    def Deselected(self, state=False):
        self.selected = state





# django-simple-history.
# from simple_history.models import HistoricalRecords
# https://django-simple-history.readthedocs.io/en/latest/
# django-simple-history almacena el estado del modelo
# Django en cada creación / actualización / eliminación.
Historical = HistoricalRecords


conteo = 0

class ModelBase(text.Text):
    """
    Clase con métodos comunes para heredar en los modelos.
    """

    def __str__(self):
        return "ModelBase"

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def print_title(self):
        return str(self)

    def save(self, *args, **kwargs):
        """
        Método 'save' de los modelos en Django.
        """
        save = super().save(*args, **kwargs)
        return save

    def save_without_historical_record(self, *args, **kwargs):
        """
        If you want to save a model without a historical record.

        https://django-simple-history.readthedocs.io/en/latest/querying_history.html
        
        """
        print(f"{self} | Guardando sin history_record")
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def clean(self, *args, **kwargs):
        """
        Método 'clean' de los modelos en Django.
        """
        clean = super().clean(*args, **kwargs)
        # Lo reemplazamos por:
            # MIDDLEWARE = [
                # ...
                # 'simple_history.middleware.HistoryRequestMiddleware',
            # ]
        # Almacenamos en el campo 'history' de la app 'django-simple-history'
        # el usuario que módificó, ya que la app en custión no lo hace.
        #try:
        #    history = self.history.last()
        #    if (history.history_type == "+"):
        #        history.history_user = self.create_user
        #    else:
        #        history.history_user = self.update_user
        #    history.save()
        #except (BaseException):
        #    pass
        return clean

    def getattr(self, name, default="__raise_exception__"):
        """
        Un getattr ideal.

        Permitiendo obtener el valor de un campo relacionado a este objeto.
        Por ejemplo: Suponiendo que el objeto en cuestión tiene un campo
        ForeignKey llamado 'documento', el cual a su vez tiene un campo
        ForeignKey llamado 'almacen':
            obj.getattr('documento__almacen__nombre')

        Parameters:
            name (str): Nombre del attributo o field.

        Returns:
            getattr(name)
        """
        # Lanzará excepción si no se encuentra el primer nombre.
        # Pero para el resto, devolverá el valor del argumento 'default' si se indica.
        names = name.split("__")
        attr = self
        for n in names:
            if (hasattr(attr, n)):
                attr = getattr(attr, n, None)
            else:
                if (default != "__raise_exception__"):
                    return default
                raise AttributeError(
                f"Error en {repr(self)} obteniendo el atributo '{name}'. {repr(attr)} no tiene un atributo llamado '{n}'.")
        return attr

    def GetBarcode(self, code=None, strtype="code128"):
        """
        Obtiene el código de barras de este objeto.
        según su salida str.

        Parameters:
            code (str): código a obtener (opcional) (default = self)

            strcode (str): tipo de código.

        Returns:
            get_barcode(code=str(code or self), strtype=strtype)
        """
        try:
            return get_barcode(str(code or self), strtype=strtype)
        except (BaseException) as e:
            return e

    def GetThis(self):
        """
        Obtiene este objeto desde la base de datos.

        Útil en caso de modificaciones, para comparar los datos anteriores con 
        los que se pretenden establecer.
        """
        if self.pk:
            return self.__class__.objects.get(pk=self.pk)

    def GetDetail(self, include_parents=False, include_hidden=False):
        """
        Obtiene el detalle del objeto.
        """
        detail = fuente.detail.Detail(self)
        detail.SetFieldsDefault(include_parents=include_parents, include_hidden=include_hidden)
        return detail

    def ToDict(self, to_json=False, for_json=False, no_json_serialize_to_str=False):
        """
        Obtiene un diccionario con los nombres de los campos como claves,
        y otro diccionario como valores, con algunos valores de la field.

        to_json = True: devolverá un objeto Json.

        for_json = True: devolverá un diccionario válido para ser serializado a json.

        no_json_serialize_to_str = True: Para los campos que no sean serializados a json,
            serán convertidos a string mediante str(value).
        """
        out = {}
        fields = self.GetFields()
        for field in fields:

            value = getattr(self, field.name, None)

            if (to_json) or (for_json):

                if (isinstance(value, Decimal)):
                    value = float(value)

                # Los campos que no se puedan serializar a Json,
                # no serán incluidos.
                try:
                    json.dumps(value)
                except (TypeError):
                    if (not no_json_serialize_to_str):
                        value = str(value)
                    else:
                        continue

            out[field.name] = {
                "name": field.name,
                "verbose_name": field.verbose_name,
                "value": value,
                "editable": field.editable,
            }

        if (to_json):
            return json.dumps(out)
        return out

    def ToJson(self):
        """
        Obtiene un objeto tipo Json con los datos de los campos.
        """
        return self.ToDict(to_json=True)

    @classmethod
    def GetImg(self, default=""):
        """
        Trata de obtener la imagen asignada
        a este objecto o modelo.
        De no encontrar una ruta de imagen, devolverá
        el valor del parámetro default.
        """
        # Buscamos una field (campo) de tipo image o file
        #  que se hay declarado con algunos de estos nombres.
        img = getattr(self, "image.url", getattr(self, "img.url", None))

        # Buscamos en las variables del módulo fuente.var, alguna que
        # coincida con el nombre del modelo en cuestión. Las variables de
        # imagenes están declaradas en mayúsculas y empiezan con 'IMG_'.
        # Ejemplo: IMG_MODELNAME
        if (not img):
            img = vars().get(f"IMG_{self.__class__.__name__.upper()}", "")
        return img

    @classmethod
    def GetFields(self, solo_editables=False):
        """
        Obtiene un listado con los campos del modelo.
        """
        out = self._meta.fields
        if (solo_editables):
            out = [f for f in out if f.editable]
        return out

    @classmethod
    def GetFieldsEditables(self):
        """
        Obtiene un listado con los campos editables del modelo.
        """
        return self.GetFields(True)

    @classmethod
    def GetFieldsNames(self, solo_editables=False):
        """
        Obtiene un listado con los nombres de los campos
        en el modelo.
        """
        return [f.name for f in self.GetFields(solo_editables=solo_editables)]

    @classmethod
    def GetFieldsNamesEditables(self):
        """
        Obtiene un listado con los modelos de los campos
        editables del modelo.
        """
        return self.GetFieldsNames(True)

    @classmethod
    def GetFieldsNamesDisplay(self, solo_editables=False):
        """
        Obtiene un listado con los nombres de los campos
        visibles tal como son mostrados al usuario.
        """
        return [f.verbose_name for f in self.GetFields(solo_editables=solo_editables)]

    @classmethod
    def GetFieldsNamesDisplayEditables(self):
        """
        Obtiene un listado con los nombres de los campos
        editables del modelo, tal como son mostrados al usuario.
        """
        return self.GetFieldsNamesDisplay(True)

    @classmethod
    def GetFieldsForReport(self, json_clean=False, excludes=["tags", "password"],
    include_parents=False, exclude_add_relations_model_fields=False):
        """
        Obtiene un diccionario con los nombres de los campos como
        sus claves, y una lista con información sobre dicho campo
        como el valor de cada item. Esta información será utlizada
        por UNOLET para mostrar los campos en las listas de
        objetos y en los reportes.

        Podemos configurar esto en cada modelo, agregando este método.

        De forma predeterminada, los campos a mostrar serían solo los
        campos definidos en el modelo marcados como editables.

        La mayoría de los campos del modelo user.User están excluidos por
        motivo de seguridad.

        Parameters:
            json_clean (bool): Si es True, limpia los items que no sean json serializables.

            excludes (list): Una lista de nombres de campos que desea excluir. De forma
            predeterminada excluimos el campo 'tags'.

            include_parents (bool): si es True, incluirá también los campos de sus relaciones.

            exclude_add_relations_model_fields (bool): Si es True, no serán incluidos los
            campos del modelo de las relaciones ForeignKey, etc. Esto es para evitar
            una recursión, ya que se llama a este método para extraer dichos campos.

        Returns:
            dict: Un diccionario con cada field agregada.
        """
        if (not excludes):
            excludes = []

        out = report.Report()
        fields = self.GetFields()

        for field in fields:
            # Algunos campos de algunos modelos no están incluidos
            # por razones de seguridad. Un ejemplo de ello es el
            # modelo usuario, cuyo único campo permitido es el
            # nombre de usuario y el nombre real.
            if ("user" in (self.__name__.lower(), self.__class__.__name__.lower())):
                if (not field.name in ("username", "first_name", "last_name")):
                    continue

            # Fields que se excluirán.
            if (field.name in excludes):
                continue

            item = report.Field({
                "field": field, # Es posible agregar métodos del modelo en vez de campos.
                "name": field.name,
                "verbose_name": field.verbose_name,
                "help_text": field.help_text,
                "value": "",
                "css_class": [], # Clases CSS que serán aplicadas al valor en la plantilla.
                "template_filters": [], # filtros que serán aplicados al valor en la plantilla.
                "data_type": var.STR,
                "is_number": False,
                "is_method": False, # Indica si apunta a un método del objeto.
            })
            if (isinstance(field, models.IntegerField)):
                item["css_class"].append("text-right")
                item["template_filters"].append("intcomma")
                item["data_type"] = var.INT
                item["is_number"] = True
            elif (isinstance(field, models.FloatField)):
                item["css_class"].append("text-right")
                item["template_filters"].append("intcomma")
                item["data_type"] = var.FLOAT
                item["is_number"] = True
            elif (isinstance(field, models.DecimalField)):
                item["css_class"].append("text-right")
                item["template_filters"].append("intcomma")
                item["data_type"] = var.DECIMAL
                item["is_number"] = True
            elif (isinstance(field, models.DateField)):
                item["data_type"] = var.DATE
            elif (isinstance(field, models.DateTimeField)):
                item["data_type"] = var.DATETIME
            elif (isinstance(field, (models.CharField, models.TextField))):
                item["template_filters"].append("text-truncate")
                item["data_type"] = var.STR
            elif (isinstance(field, models.AutoField)):
                item["data_type"] = var.INT
            elif (isinstance(field, models.ForeignKey)):
                item["data_type"] = var.FOREIGN_KEY
                item["model"] = field.related_model
                item["model_name"] = item["model"]._meta.model_name
                item["app_label"] = item["model"].__module__.split(".")[0] # app_label.models

                if (include_parents):
                    # Incluimos, junto a las demás fields, las fields de los modelos
                    # relacionados con este, a travez de ForeignKey.
                    # Estas fields tendrán una estructura de nombre: field__relactionfield.
                    relations = item["model"].GetFieldsForReport(json_clean=json_clean,
                        exclude_add_relations_model_fields=True, include_parents=False)
                    for relitem in relations.values():
                        relitem["name"] = f"{field.name}__{relitem['name']}" # field__relfield.
                        relitem["verbose_name"] = f"{field.verbose_name} | {relitem['verbose_name']}" # Field | RelationField.
                        out[relitem["name"]] = relitem

                if (not exclude_add_relations_model_fields):
                    if (hasattr(item["model"], "GetFieldsForReport")):
                        item["fields"] = item["model"].GetFieldsForReport(
                            json_clean=json_clean,
                            exclude_add_relations_model_fields=True)

            item["css_class_string"] = " ".join(item["css_class"])

            if json_clean:
                item = json.clean(item, remove=False)

            out[field.name] = item
        return out

    def GetHistory(self):
        """
        Obtiene el historial de cambios realizadas al objeto
        desde su creación, con 'django-simple-history'.
        """
        try:
            return self.history.all()
        except (AttributeError):
            return None

    def GetHistoryAll(self):
        """
        Obtiene el historial de cambios realizados a todos
        los objetos del modelo, con 'django-simple-history'.
        """
        try:
            return self.history.model.objects.all()
        except (AttributeError):
            return None








class listview_decorator(text.Text):

    def __init__(self, queryset=None, reporte=None, limit=100, model=None, otros_filtros=[]):
        if queryset != None:
            self.queryset = queryset
            self.model = queryset.model
        elif model:
            self.queryset = model.objects.all()
            self.model = model
        self.reporte = reporte
        self.limit = limit or 100
        self.otros_filtros = otros_filtros or [] # Nombres de los parametros pasados por request.GET en los que también se pretende filtrar.


    def __call__(self, view, *args, **kwargs):

        self.submenu_nueva_version = context_decorator(*args, **kwargs)

        def func(request, *args, **kwargs):
            q = request.GET.get("q") or None
            field = request.GET.get("field")
            page = request.GET.get("page") or 1
            limit = request.GET.get("limit") or self.limit
            qs = self.queryset

            if (q) and (field) and (field != "tags"):
                qs = qs.filter(**{"%s__icontains" % field: self.GetTag(q, False)})
            elif (q):
                qs = qs.filter(tags__icontains=self.GetTag(q, False))

            if self.otros_filtros:
                dic = {}
                for _name in self.otros_filtros:
                    _value = request.GET.get(_name)
                    if _value in (None, ""):
                        continue
                    dic[_name] = _value
                qs = qs.filter(**dic)

            paginator = Paginator(qs, limit)
            page_obj = paginator.get_page(page)

            if self.reporte:
                reporte = self.reporte(queryset=page_obj.object_list)
                kwargs["reporte"] = reporte

            kwargs["object_list"] = page_obj.object_list
            kwargs["queryset"] = page_obj.object_list
            kwargs["model"] = self.model
            kwargs["paginator"] = paginator
            kwargs["page_obj"] = page_obj
            kwargs["page_num"] = page
            kwargs["submenu_nueva_version"] = self.submenu_nueva_version
            return view(request, *args, **kwargs)
        return func




def any_permission_required(*args):
    """
    A decorator which checks user has any of the given permissions.
    permission required can not be used in its place as that takes only a
    single permission.
    """
    def test_func(user):
        for perm in args:
            if user.has_perm(perm):
                return True
        return False
    return user_passes_test(test_func)
