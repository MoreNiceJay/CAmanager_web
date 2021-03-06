# Generated by Django 2.0.4 on 2019-03-29 09:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('genkey', '0008_auto_20190328_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuer',
            name='algorithm',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issuer',
            name='organization_unit',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issuer',
            name='private_key',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='issuer',
            name='valid_period',
            field=models.IntegerField(),
        ),
    ]
