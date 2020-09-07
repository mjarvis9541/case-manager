# Generated by Django 3.1 on 2020-09-04 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productivity', '0004_casetype_description'),
        ('accounts', '0003_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='productivity.department'),
        ),
    ]