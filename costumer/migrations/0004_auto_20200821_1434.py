# Generated by Django 3.0.8 on 2020-08-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costumer', '0003_auto_20200821_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumer',
            name='job',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='job'),
        ),
    ]
