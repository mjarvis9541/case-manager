# Generated by Django 3.1 on 2020-09-08 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0006_auto_20200906_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='department',
            name='date_modified',
        ),
    ]
