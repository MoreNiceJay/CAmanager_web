# Generated by Django 2.0.4 on 2019-03-26 01:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('genkey', '0003_remove_ca_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='ca',
            name='domain',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]