# Generated by Django 3.1.3 on 2020-12-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='information_content',
            field=models.TextField(blank=True, verbose_name='Información: Contenido'),
        ),
        migrations.AddField(
            model_name='setting',
            name='information_title',
            field=models.CharField(blank=True, max_length=70, verbose_name='Información: Título'),
        ),
    ]
