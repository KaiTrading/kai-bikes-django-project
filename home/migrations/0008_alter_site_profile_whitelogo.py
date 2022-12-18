# Generated by Django 3.2 on 2022-09-09 15:14

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_site_profile_whitelogo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site_profile',
            name='whitelogo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='whitelogo'),
        ),
    ]
