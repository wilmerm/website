# Generated by Django 3.1.3 on 2021-02-13 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_auto_20210209_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que leyó'),
        ),
    ]
