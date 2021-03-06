# Generated by Django 3.2.5 on 2021-07-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210302_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.URLField(blank=True, verbose_name='URL de la imagen'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imagen 1'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imagen 2'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, upload_to='store/item/', verbose_name='Imagen 3'),
        ),
    ]
