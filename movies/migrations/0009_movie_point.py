# Generated by Django 2.1.12 on 2020-06-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20200613_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]