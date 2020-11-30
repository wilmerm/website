import os

from django import template
from django.conf import settings



register = template.Library()




@register.inclusion_tag("tags/icon.html")
def svg(filename: str, size: str = "32px", fill=None) -> dict:
    """
    Retorna el contenido del archivo SVG con el nombre indicado.

    Nota: retorna el contenido, no la ruta, en un archivo .SVG.
    
    """
    path = settings.BASE_DIR / f"static/img/icons/{filename}.svg"
    svg = open(path, "r").read()
    return {"svg": svg, "size": size, "fill": fill, "filename": filename}