# Generated by Django 3.0.8 on 2020-09-19 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specification', '0003_auto_20200919_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specification',
            name='field_name',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='field_value',
        ),
    ]
