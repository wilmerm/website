# website
Sitio web genérico, capaz de adaptarlo a cualquier tipo de negocio o diseño.


## Dependencias:
* easy_thumbnails
* django-colorfield
* django-tinymce
* django-bootstrap4
* requests (Requerida por google-auth)
* google-auth https://google-auth.readthedocs.io/en/latest/


```bash
pip install easy_thumbnails
pip install django-colorfield
pip install django-tinymce
pip install django-bootstrap4 (Será reemplazado por Bootstrap5)
pip install django-bootstrap-v5
pip install requests
pip install --upgrade google-auth
```


## Instalación:
Se está trabajando con django.sites y con un modelo de usuario personalizado, de
modo que, para la primera implementación, es necesario comentar las demás 
aplicaciones del proyecto en el settings y comentar las urls en app.urls:

1 - Comente las aplicaciones 'base' y 'store' en app.settings.base.
2 - Comente las urls en app.urls excepto las de 'admin'.
3 - Ejecute python manage.py migrate.
4 - Descomente las aplicaciones y las urls que comentó en el paso 1.
5 - Ejecute python manage.py makemigrations
6 - Ejecute python manage.py migrate

El archivo 'app.settings.localhost.py' será el setting para la versión de 
desarrollo. A partír de ahi se podrán crear los demás settings de los diferentes
sitios donde correrá el proyecto.

