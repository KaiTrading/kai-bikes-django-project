# Generated by Django 3.0.7 on 2022-11-02 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20221102_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coustomer_text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Heading', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=2000)),
                ('link_text', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=180)),
            ],
        ),
    ]
