# Generated by Django 3.2 on 2022-09-03 14:35

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site_profile',
            name='logo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='logo'),
        ),
    ]
