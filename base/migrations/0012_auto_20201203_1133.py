# Generated by Django 3.1.3 on 2020-12-03 11:33

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_sampleimage_samplevideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleimage',
            name='image',
            field=models.ImageField(upload_to='sapleimage', validators=[base.models.validate_image_size], verbose_name='Imágen'),
        ),
    ]
