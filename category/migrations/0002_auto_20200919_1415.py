# Generated by Django 3.0.8 on 2020-09-19 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specification', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='category.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to='specification.Specification'),
        ),
    ]
