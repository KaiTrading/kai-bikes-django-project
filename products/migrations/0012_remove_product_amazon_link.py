# Generated by Django 3.0.7 on 2022-12-17 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20221217_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='amazon_link',
        ),
    ]
