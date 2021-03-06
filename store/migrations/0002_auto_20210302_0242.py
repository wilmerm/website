# Generated by Django 3.1.3 on 2021-03-02 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-is_featured', '-available'], 'verbose_name': 'artículo', 'verbose_name_plural': 'artículos'},
        ),
        migrations.AlterModelOptions(
            name='storesetting',
            options={'verbose_name': 'configuración de tienda', 'verbose_name_plural': 'configuración de tienda'},
        ),
        migrations.AddField(
            model_name='storesetting',
            name='show_items_without_price',
            field=models.BooleanField(default=False, help_text='muestra los artículos aunque no tengan precio.', verbose_name='mostrar artículos in precio'),
        ),
        migrations.AlterField(
            model_name='storesetting',
            name='currency_symbol',
            field=models.CharField(blank=True, help_text='símbolo de la moneda en que están los precios de los items.', max_length=5, verbose_name='moneda'),
        ),
        migrations.AlterField(
            model_name='storesetting',
            name='policies',
            field=models.CharField(blank=True, help_text='texto que contine una versión corta de las políticas, términos y condiciones de al compara a través de la tienda en línea. Este texto aparecerá en las ordenes impresas que realicen los clientes a través la tienda en línea.', max_length=700, verbose_name='políticas de la tienda en línea'),
        ),
        migrations.AlterField(
            model_name='storesetting',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=18, help_text='porcentaje de impuesto a cargar a los artículos.', max_digits=5, verbose_name='impuesto porcentaje'),
        ),
    ]
