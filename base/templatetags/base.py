import os
import datetime
import re

from django import template
from django.conf import settings
from fuente import text




register = template.Library()




@register.simple_tag
def vue(content):
    """
    Devuelve el contenido encerrado en dos llaves {{content}}.
    Útil para mostrar contenido de los frameworks VueJs y AngularJs.

    """
    return "{{" + content + "}}"



@register.inclusion_tag("tags/icon.html")
def svg(filename: str, size: str = None, fill: str = None, 
    id: str = None) -> dict:
    """
    Retorna el contenido del archivo SVG con el nombre indicado.

    Nota: retorna el contenido, no la ruta, en un archivo .SVG.

    Parameters:
        filename (str): Nombre del archivo o ruta. Si se indica el nombre del 
        archivo, buscará dentro de los directorios static/img/* predeterminados.
        Si se indica una ruta, tendrá que empezar por /static/*

        size (str): El size se pasará a las opciones CSS (width, height) tal y 
        como se especifiquen, por lo cual es conveniente indicar su tipo de 
        medida (ejemplos '32px', '2rem', etc.).

        fill (str): CSS color que se pasará a la opción fill para pintar la 
        imagen.

    """
    fill = fill or 'var(--primary)'


    if "/" in filename:
        path = filename
        if not ".svg" in path:
            path += ".svg"
        if path[0] == "/":
            path = path.replace("/", "", 1)
        path = settings.BASE_DIR / path
        svg = open(path, "r").read()
        filename = filename.split("/")[-1].replace(".", "-")
    else:
        path1 = settings.BASE_DIR / f"static/img/icons/{filename}.svg"
        path2 = settings.BASE_DIR / f"static/img/others/{filename}.svg"

        try:
            svg = open(path1, "r").read()
        except (FileNotFoundError):
            svg = open(path2, "r").read()

    # Eliminamos los saltos de línea y espacios extras.
    svg = " ".join(svg.replace("\n", " ").split())

    if not id:
        id = f"id-svg-{filename}-fill-{fill}-size-{size}-{datetime.datetime.today()}"
        id = text.Text.FormatCodename(id)

    if (not " width=" in svg) and (size != None):
        svg = re.sub(r'<svg\s', f'<svg width="{size}" ', svg, count=1)
    elif size != None:
        svg = re.sub(r'\swidth=(["\']).*?["\']\s', f' width="{size}" ', svg, 
        count=1)
    
    if (not " height=" in svg) and (size != None):
        svg = re.sub(r'<svg\s', f'<svg height="{size}" ', svg, count=1)
    elif size != None:
        svg = re.sub(r'\sheight=(["\']).*?["\']\s', f' height="{size}" ', svg, 
        count=1)

    if (not " fill=" in svg):
        svg = re.sub(r'<svg\s', f'<svg fill="{fill}" ', svg, count=1)
    else:
        svg = re.sub(r'\sfill=(["\']).*?["\']\s', f' fill="{fill}" ', svg, 
        count=1)

    return {"svg": svg, "size": size, "fill": fill, "filename": filename, 
        "id": id}