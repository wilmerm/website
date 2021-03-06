# Generated by Django 3.1.3 on 2021-02-13 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_message_read_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_note',
            field=models.CharField(blank=True, max_length=300, verbose_name='nota'),
        ),
        migrations.AlterField(
            model_name='message',
            name='read_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='usuario que leyó'),
        ),
    ]
