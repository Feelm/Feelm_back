# Generated by Django 2.1.12 on 2020-06-13 06:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0005_auto_20200613_1409'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Movie_Star_Point',
            new_name='MovieStarPoint',
        ),
    ]
