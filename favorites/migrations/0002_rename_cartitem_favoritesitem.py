# Generated by Django 3.2.4 on 2021-06-15 20:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItem',
            new_name='FavoritesItem',
        ),
    ]
