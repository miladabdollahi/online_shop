# Generated by Django 3.0.8 on 2020-09-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specification', '0002_auto_20200919_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specification',
            name='field_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='name of field'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='field_value',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='value of field'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='name of specification'),
        ),
    ]
