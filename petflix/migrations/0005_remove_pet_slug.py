# Generated by Django 5.1.5 on 2025-01-26 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petflix', '0004_pet_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='slug',
        ),
    ]
