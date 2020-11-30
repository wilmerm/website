import os
import datetime
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Locales
from .paises import *


STATIC_URL = "/static/"
STATIC_ROOT = ""
MEDIA_ROOT = ""
MEDIA_URL = "/media/"
BASE_DIR = ""

try:
    from django.conf import settings
except (BaseException) as e:
    print(e)
try:
    STATIC_URL = str(settings.STATIC_URL)
except (BaseException) as e:
    print(e)
try:
    STATIC_ROOT = str(settings.STATIC_ROOT)
except (BaseException) as e:
    print(e)
try:
    MEDIA_ROOT = str(settings.MEDIA_ROOT)
except (BaseException) as e:
    print(e)
try:
    MEDIA_URL = str(settings.MEDIA_URL)
except (BaseException) as e:
    print(e)
try:
    BASE_DIR = str(settings.BASE_DIR)
except (BaseException) as e:
    print(e)



PRIMER_NUMERO_DE_CUENTA = "10221110"
PRIMER_NUMERO_DE_CLIENTE = "10102020"


FILE_EXPORT = os.path.join(MEDIA_ROOT, "file_export.csv")
FILE_EXPORT_URL = MEDIA_URL + "file_export.csv"



# PERSONAS -----------------------------------------------------------

MASCULINO = "M"
FEMENINO = "F"
NO_DEFINIDO = "ND"
SEXO_CHOICES = (
    (MASCULINO, _("Masculino")),
    (FEMENINO, _("Femenino")),
    (NO_DEFINIDO, _("No definido")),
)


SOLTERO = "SOLTERO"
CASADO = "CASADO"
UNION_LIBRE = "UNION_LIBRE"
OTRO = "OTRO"
ESTADO_CIVIL_CHOICES = (
    (SOLTERO, _("Soltero")),
    (CASADO, _("Casado")),
    (UNION_LIBRE, _("Unión libre")),
    (OTRO, _("Otro")),
)



# IDENTIFICACIÓN -----------------------------------------------------

CEDULA = "CEDULA"
PASAPORTE = "PASAPORTE"
RNC = "RNC"
OTRO = "OTRO"
IDENTIFICACION_CHOICES = (
    (CEDULA, _("Cédula")),
    (RNC, _("RNC")),
    (PASAPORTE, _("Pasaporte")),
    (OTRO, _("Otro")),

)


# CONTABILIDAD -------------------------------------------------------

DOP = "DOP"
USD = "USD"
EUR = "EUR"
CAD = "CAD"
GSB = "GSB"
MONEDA_CHOICES = (
    (DOP, _("DOP: Peso dominicano")),
    (USD, _("USD: Dólar estadounidense")),
    (EUR, _("EUR: Euro")),
    (CAD, _("CAD: Dólar canadiense")),
    (GSB, _("GSB: Libra esterlina")),
)

EFECTIVO = "EF"
CUENTA_CORRIENTE = "CC"
CUENTA_AHORROS = "CA"
PRESTAMO = "PR"
TARJETA_CREDITO = "TC"
TARJETA_DEBITO = "TD"
CUENTA_CHOICES = (
    (EFECTIVO, _("Efectivo")),
    (CUENTA_CORRIENTE, _("Cuenta corriente")),
    (CUENTA_AHORROS, _("Cuenta de ahorros")),
    (PRESTAMO, _("Préstamo")),
    (TARJETA_CREDITO, _("Tarjeta de crédito")),
    (TARJETA_DEBITO, _("Tarjeta de débito")),
)

EFECTIVO = "EFECTIVO"
CUENTA = "CUENTA"
TARJETA = "TARJETA"
PAYPAL = "PAYPAL"
BITCOIN = "BITCOIN"
CHEQUE = "CHEQUE"
MODOS_DE_PAGO = (
    (EFECTIVO, _("Efectivo")),
    (CUENTA, _("Cuenta")),
    (TARJETA, _("Tarjeta de crédito")),
    (PAYPAL, _("Paypal")),
    (BITCOIN, _("Bitcoin")),
    (CHEQUE, _("Cheque")),
)


CUOTA_FIJA = "FIJA"
CUOTA_VARIABLE = "VARIABLE"
CUOTA_TIPOS = (
    (CUOTA_FIJA, _("Cuota fija")),
    (CUOTA_VARIABLE, _("Cuota variable")),
)


DESEMBOLSO = "DESEMBOLSO"
PAGO = "PAGO"
TRANSFERENCIA = "TRANSFERENCIA"
TRANSACCION_TIPO = (
    (PAGO, _("Pago")),
    (DESEMBOLSO, _("Desembolso")),
    (TRANSFERENCIA, _("Transferencia")),

)

ENTRADA = "ENTRADA"
SALIDA = "SALIDA"
TRANSFERENCIA = "TRANSFERENCIA"
COTIZACION = "COTIZACION"
ORDEN = "ORDEN"
ENTRADA_SALIDA_CHOICES = (
    (ENTRADA, _("Entrada")),
    (SALIDA, _("Salida")),
    (TRANSFERENCIA, _("Transferencia")),
    (COTIZACION, _("Cotización")),
    (ORDEN, _("Orden")),
)

PORCENTAJE = "PORCENTAJE"
FIJO = "FIJO"
VALOR_TIPO = (
    (PORCENTAJE, _("Porcentaje")),
    (FIJO, _("Fijo")),
)


CREDITO = "CREDITO"
CONTADO = "CONTADO"
CONDICION_CHOICES = (
    (CREDITO, _("Crédito")),
    (CONTADO, _("Contado")),
)


# FECHAS ------------------------------------------------------------

DIARIO = "DIARIO"
SEMANAL = "SEMANAL"
QUINCENAL = "QUINCENAL"
MENSUAL = "MENSUAL"
ANUAL = "ANUAL"
PERIODO_CHOICES = (
    (DIARIO, _("Diario")),
    (SEMANAL, _("Semanal")),
    (QUINCENAL, _("Quincenal")),
    (MENSUAL, _("Mensual")),
    (ANUAL, _("Anual")),
)


# INFORMÁTICA ------------------------------------------------------

class Undefined(object):
    """Objeto de valor indefinido"""

    @classmethod
    def __str__(self):
        return _("Indefinido")

    @classmethod
    def __repr__(self):
        return self.__class__.__name__


TUPLE = "TUPLE"
LIST = "LIST"
DICT = "DICT"
INT = "INT"
FLOAT = "FLOAT"
DECIMAL = "DECIMAL"
STR = "STR"
BOOL = "BOOL"
DATE = "DATE"
DATETIME = "DATETIME"
HTML_IMAGE = "HTML_IMAGE"
FOREIGN_KEY = "FOREIGN_KEY"
UNDEFINED = Undefined()

TIPO_DE_DATOS_CHOICES = (
    (STR, _("Texto")),
    (INT, _("Número entero.")),
    (FLOAT, _("Número de coma flotante.")),
    (DECIMAL, _("Número decimal")),
    (TUPLE, _("Tupla")),
    (LIST, _("Lista")),
    (DICT, _("Diccionario")),
    (BOOL, _("Falso o Verdadero")),
    (DATE, _("Fecha")),
    (DATETIME, _("Fecha y hora")),
    (HTML_IMAGE, _("Imágen HTML")), # Ruta a un archivo de imágen.
    (UNDEFINED, _("Indefinido")),
)




# ----------------------------------------------------------
# NOMBRES DE PARÁMETROS ÚTILES PARA SER UTILIZADOS EN URL SIN
# QUE EL USUARIO TENGA QUE SABER EL NOMBRE DEL PARÁMETRO.
# ----------------------------------------------------------

PARAM_1 =                  "1hew5roit3kjjpfd6eepooiws5qaas1sffpoe512ew64re544wf"
PARAM_2 =                  "2oijpfd6dejr73nnfkan38845unkakmfhaoladipqusffpoe51f"
PARAM_3 =                  "3t3jpfdoiwakajjdsfhasdfgghsqas1sffoe64rasdfggh544wf"
PARAM_4 =                  "4ws5o5445a1145a5fjjgjhajhy67171930j3838739jhnajdhwa"
PARAM_5 =                  "5roadfjjaiofhrjhnjasdfyajlf5654asdfjhalhfye5eyhayfj"
PARAM_6 =                  "6dhfhahladf7yuqherafiuhfjadfy7qoeejejeghshgsjdi9ija"




# IMÁGENES. ----------------------------------------------------------
# base

PATH_ROOT_IMG = BASE_DIR + STATIC_URL + "img/"
PATH_IMG = STATIC_URL + "img/"
IMG_DEFAULT = PATH_IMG + "base/default.svg"

#ESTABLECIENDO LAS IMAGENES...
IMG_ADUANA = '/static/img/aduana.svg'
IMG_CONTABILIDAD = '/static/img/contabilidad.svg'
IMG_DOCUMENTO = '/static/img/documento.svg'
IMG_DOCUMENTO_FACTURA = IMG_DOCUMENTO
IMG_EMPRESA = '/static/img/empresa.svg'
IMG_EMPRESA_UNDEFINED = "/static/img/base/my-business-undefined.png"
IMG_PRESTAMO = "/static/img/prestamo.svg"
IMG_PUNTOVENTA = "/static/img/puntoventa.svg"


# MÓDULOS.------------------------------------------
IMG_USER = PATH_IMG + "modules/user.svg"
IMG_USER_LIST = PATH_IMG + "modules/user_list.svg"
IMG_USER_ADD = PATH_IMG + "modules/user_add.svg"

IMG_ALMACEN = PATH_IMG + "modules/almacen.svg"
IMG_ALMACEN_LIST = PATH_IMG + "modules/almacen_list.svg"
IMG_ALMACEN_ADD = PATH_IMG + "modules/almacen_add.svg"

IMG_ARTICULO = PATH_IMG + "modules/articulo.svg"
IMG_ARTICULO_LIST = PATH_IMG + "modules/articulo_list.svg"
IMG_ARTICULO_ADD = PATH_IMG + "modules/articulo_add.svg"

IMG_ARTICULO_FAMILIA = PATH_IMG + "modules/articulo_familia.svg"
IMG_ARTICULO_FAMILIA_LIST = PATH_IMG + "modules/articulo_familia_list.svg"
IMG_ARTICULO_FAMILIA_ADD = PATH_IMG + "modules/articulo_familia_add.svg"

IMG_ARTICULO_GRUPO = PATH_IMG + "modules/articulo_grupo.svg"
IMG_ARTICULO_GRUPO_LIST = PATH_IMG + "modules/articulo_grupo_list.svg"
IMG_ARTICULO_GRUPO_ADD = PATH_IMG + "modules/articulo_grupo_add.svg"

IMG_ARTICULO_PRICINGPOLICY = PATH_IMG + "modules/articulo_pricingpolicy.svg"

IMG_PERSONA = PATH_IMG + "modules/persona.svg"
IMG_PERSONA_LIST = PATH_IMG + "modules/persona_list.svg"
IMG_PERSONA_ADD = PATH_IMG + "modules/persona_add.svg"
IMG_PERSONA_BALANCE = PATH_IMG + "modules/persona_balance.svg"
IMG_CLIENTE = IMG_PERSONA

IMG_AUTORIZACION_NCF = PATH_IMG + "modules/autorizacion_ncf.svg"
IMG_AUTORIZACION_NCF_LIST = PATH_IMG + "modules/autorizacion_ncf_list.svg"
IMG_AUTORIZACION_NCF_ADD = PATH_IMG + "modules/autorizacion_ncf_add.svg"

IMG_NCF = PATH_IMG + "modules/ncf.svg"
IMG_NCF_LIST = PATH_IMG + "modules/ncf_list.svg"
IMG_NCF_TIPO = PATH_IMG + "modules/tipo_ncf.svg"
IMG_NCF_TIPO_LIST = PATH_IMG + "modules/tipo_ncf_list.svg"
IMG_IMPUESTO = PATH_IMG + "modules/impuesto.svg"
IMG_IMPUESTO_LIST = PATH_IMG + "modules/impuesto_list.svg"
IMG_IMPUESTO_ADD = PATH_IMG + "modules/impuesto_add2.svg"

IMG_INVENTARIO = PATH_IMG + "modules/inventario.svg"

IMG_RRHH = PATH_IMG + "modules/rrhh.svg"
IMG_EMPLOYEE = PATH_IMG + "modules/employee.svg"

IMG_MEDIDA_GRUPO = PATH_IMG + "modules/medida_grupo.svg"
IMG_MEDIDA_GRUPO_ADD = PATH_IMG + "modules/medida_grupo_add.svg"
IMG_MEDIDA_UNIDAD = PATH_IMG + "modules/medida_unidad.svg"
IMG_MEDIDA_UNIDAD_ADD = PATH_IMG + "modules/medida_unidad_add.svg"

IMG_MONEDA = PATH_IMG + "modules/moneda.svg"



# ---------------------------------------------------




IMG_FORMADEPAGO = "/static/img/formadepago.svg"
IMG_MEDIODEPAGO = "/static/img/credit-card.svg"

IMG_ADD = '/static/img/base/add.svg'
IMG_BACK = '/static/img/base/back.svg'
IMG_CALC = '/static/img/base/calc.svg'
IMG_CANCEL = '/static/img/base/cancel.svg'
IMG_CARGANDO = '/static/img/base/cargando.gif'
IMG_CLOSE = '/static/img/base/close.svg'
IMG_DELETE = '/static/img/base/delete.svg'
IMG_EDIT = '/static/img/base/edit.svg'
IMG_HOME = "/static/img/base/home.svg"
IMG_IDENTIFICATION = '/static/img/base/identification.svg'

IMG_LIST = '/static/img/base/list.svg'
IMG_BARCODE = '/static/img/base/barcode.svg'
IMG_LOGO = '/static/img/base/logo.svg'
IMG_MENU = '/static/img/base/menu.svg'
IMG_MESSAGE = '/static/img/base/message.svg'
IMG_MESSAGE_NEW = '/static/img/base/message_new.svg'
IMG_NEXT = '/static/img/base/next.svg'
IMG_PRINT = '/static/img/base/print.svg'
IMG_QUESTION = '/static/img/base/question.svg'
IMG_SAVE = '/static/img/base/save.svg'
IMG_SEARCH = '/static/img/base/search.svg'

# SOCIAL.
IMG_FACEBOOK = '/static/img/social/facebook.svg'
IMG_GPLUS = '/static/img/social/gplus.svg'
IMG_INSTAGRAM = '/static/img/social/instagram.svg'
IMG_LINKEDIN = '/static/img/social/linkedin.svg'
IMG_PINTERES = '/static/img/social/pinteres.svg'
IMG_TWITTER = '/static/img/social/twitter.svg'
IMG_WHATSAPP = '/static/img/social/whatsapp.svg'
IMG_YOUTUBE = '/static/img/social/youtube.svg'
IMG_VK = '/static/img/social/vk.svg'

IMG_REPORTE = "/static/img/base/reporte.svg"

IMG_SORRY = '/static/img/base/sorry.svg'
IMG_STAT = '/static/img/base/stat.svg'
IMG_STOP = '/static/img/base/stop.svg'

IMG_DANGER = "/static/img/base/danger.svg"
IMG_DANGER = "/static/img/base/warning.svg"
IMG_SUCCESS = "/static/img/base/success.svg"
IMG_INFO = '/static/img/base/info.svg'

IMG_CONTENEDOR = '/static/img/contenedor.svg'


# Iconos (bootstrap icons).
# Iconos SVG suministrados por Bootstrap desde su página web.
# Los descargamos y guardamos en la carpeta static/icons/
# Podemos hacer referencias a estas imagens como por ejemplo:
# -> icons.image_name, {{ icons.image_name }}, ...

class icon:

    def __init__(self, name, url, content):
        self.name = name
        self.url = url
        self.content = content

    def __str__(self):
        return self.url



class icons:

    @classmethod
    def __iter__(self):
        for value in self.__dict__.values():
            if (isinstance(value, icon)):
                yield value

    @classmethod
    def get_first(self, name):
        """
        Obtiene la primera coincidencia.
        """
        name = "_".join(name.split()).lower().replace("-", "_")
        try:
            return self.__dict__[name]
        except (KeyError):
            for key in self.__dict__.keys():
                if name in key:
                    return getattr(self, key, None)



def __set_icons_names(path):
    path = os.path.normpath(path)
    for f in os.listdir(path):
        p = os.path.join(path, f)
        # Si es un subdirectorio, lo recorremos también.
        if (os.path.isdir(p)):
            __set_icons_names(p)
        elif (os.path.isfile(p)):
            basename, ext = os.path.splitext(f)
            p = os.path.normpath(p)
            if (ext.lower() in (".svg", ".jpg", ".jpeg", ".bmp", ".png", ".gif")):
                name = "_".join(basename.lower().strip().split()).replace("-", "_").replace(" ", "_").replace(".", "_")

                content = open(os.path.join(p), "r").read()

                setattr(icons, name,
                icon(name=name, url=PATH_IMG + f"icons/{f}", content=content))


# Establecemos los iconos de bootstrap.
__set_icons_names(PATH_ROOT_IMG + "icons/")





# Todas las variables (esto debe ir siempre al final del archivo,
# para que tome todas las variables)

# Agregamos las variables de las aplicaciones.

for name in settings.INSTALLED_APPS:
    try:
        exec(f"from {name}.var import *")
    except (BaseException) as e:
        continue

VAR = vars().copy()


class __var:

    def __init__(self, var):
        self.var = var

    def __getattribute__(self, name):
        return object.__getattribute__(self, "var")[name]



var = __var(VAR)
