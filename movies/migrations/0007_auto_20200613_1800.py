# Generated by Django 2.1.12 on 2020-06-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20200613_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='nowplaying',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='upcoming',
            field=models.BooleanField(default=False),
        ),
    ]
