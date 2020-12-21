# Generated by Django 3.1.3 on 2020-12-18 01:29

import colorfield.fields
import django.contrib.sites.managers
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='store/brand/', verbose_name='Imágen')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'ordering': ['name'],
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='store/group/', verbose_name='Imágen')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'ordering': ['name'],
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(max_length=30, verbose_name='Referencia')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=700, verbose_name='Descripción')),
                ('image1', models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imágen 1')),
                ('image2', models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imágen 2')),
                ('image3', models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imágen 3')),
                ('color1', colorfield.fields.ColorField(blank=True, default='', max_length=18, verbose_name='Color principal')),
                ('color2', colorfield.fields.ColorField(blank=True, default='', max_length=18, verbose_name='Color secundario')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Peso')),
                ('weight_type', models.CharField(blank=True, help_text='Indique el tipo de medida para el peso indicado (Kg, Lbr, Onz, ...).', max_length=50, verbose_name='Peso (tipo)')),
                ('volumen', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Volumen')),
                ('volumen_type', models.CharField(blank=True, help_text="Indique el tipo de medida para el volumen indicado (Ejemplo 'metro cúbico').", max_length=50, verbose_name='Volumen (tipo)')),
                ('length_width', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Longitud de ancho')),
                ('length_height', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Longitud de alto')),
                ('length_depth', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Longitud de profundidad')),
                ('length_type', models.CharField(blank=True, help_text="Indique el tipo de medida para las longitudes indicadas (Ejemplo 'metro').", max_length=50, verbose_name='Longitud (tipo)')),
                ('material', models.CharField(blank=True, help_text="Tipo de material principal del cual está constituído (Ejemplo 'plástico').", max_length=50, verbose_name='Material')),
                ('capacity', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Capacidad')),
                ('capacity_type', models.CharField(blank=True, help_text='El tipo de medida para la capacidad indicada (ejemplos BTU, Watts, Voltios, Amperaje, Hz, etc.', max_length=50, verbose_name='Capacidad (tipo)')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Precio')),
                ('is_active', models.BooleanField(default=True, help_text='El artículo estará o no visible para la venta.', verbose_name='Activo')),
                ('is_featured', models.BooleanField(default=False, help_text='El artículo aparecerá en los primeros lugares de la tienda.', verbose_name='Destacado')),
                ('available', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Disponibles')),
                ('pay_tax', models.BooleanField(default=True, verbose_name='Paga impuesto')),
                ('count_search', models.IntegerField(default=0, editable=False, verbose_name='Búsquedas')),
                ('count_views', models.IntegerField(default=0, editable=False, verbose_name='Vistas')),
                ('count_taken', models.IntegerField(default=0, editable=False, verbose_name='Añadidas a la cesta')),
                ('count_sold', models.IntegerField(default=0, editable=False, verbose_name='Ventas')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('tags', models.CharField(blank=True, editable=False, max_length=700)),
            ],
            options={
                'verbose_name': 'Artículo',
                'verbose_name_plural': 'Artículos',
                'ordering': ['-is_featured', '-available'],
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='Mov',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(verbose_name='Cantidad')),
                ('price', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Precio')),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=17, verbose_name='Impuestos')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=17, verbose_name='Importe')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=17, verbose_name='Importe')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Modificación')),
            ],
            options={
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, verbose_name='Número')),
                ('note', models.CharField(blank=True, max_length=700, verbose_name='Comentario')),
                ('address', models.CharField(blank=True, max_length=700, verbose_name='Dirección')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Teléfonos')),
                ('payment_method', models.CharField(choices=[('CASH', 'Efectivo'), ('CREDIT_CARD', 'Tarjeta de crédito'), ('BANK_ACCOUNT', 'Cuenta de banco'), ('OTHER', 'Otro')], default='CASH', max_length=20, verbose_name='Forma de pago')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Modificación')),
                ('status', models.CharField(blank=True, choices=[('PROCESS', 'En proceso'), ('COMPLETE', 'Completado')], default='PROCESS', max_length=20, verbose_name='Estado')),
                ('status_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha del último estado')),
                ('accepted_policies', models.BooleanField(default=False, help_text='Al marcar esta casilla usted acepta y está de acuerdo con las políticas del sitio para compras en línea.', verbose_name='Estoy de acuerdo con las políticas del sitio')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='OrderNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('content', models.CharField(max_length=700, verbose_name='Contenido')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
            ],
            options={
                'verbose_name': 'Nota de orden',
                'verbose_name_plural': 'Notas de ordenes',
            },
        ),
        migrations.CreateModel(
            name='StoreSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax', models.DecimalField(decimal_places=2, help_text='Porcentaje de impuesto a cargar a los artículos.', max_digits=5, verbose_name='Impuesto porcentaje')),
                ('currency_symbol', models.CharField(blank=True, help_text='Símbolo de la moneda en que están los precios de los items.', max_length=5, verbose_name='Moneda')),
                ('site', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': 'Configuración de tienda',
                'verbose_name_plural': 'Configuración de tienda',
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
