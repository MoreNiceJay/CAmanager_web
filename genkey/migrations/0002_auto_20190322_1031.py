# Generated by Django 2.0.4 on 2019-03-22 01:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('genkey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ca',
            name='private_key',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ca',
            name='public_key',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
    ]
