# Generated by Django 3.1 on 2020-09-06 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productivity', '0005_auto_20200905_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_ref',
            field=models.CharField(max_length=24, verbose_name='CET Reference'),
        ),
        migrations.AlterField(
            model_name='case',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_case', to=settings.AUTH_USER_MODEL),
        ),
    ]
