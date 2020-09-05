# Generated by Django 3.1 on 2020-09-04 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0004_casetype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casetype',
            name='description',
            field=models.CharField(blank=True, help_text='Optional. Description of the task (Eg. Used for when case handlers log PPI cases, etc)', max_length=250, null=True),
        ),
    ]
