# Generated by Django 3.0.8 on 2020-09-15 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name of specification')),
                ('field_name', models.CharField(max_length=150, verbose_name='name of field')),
                ('field_value', models.CharField(max_length=250, verbose_name='value of field')),
                ('parent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='specification.Specification')),
            ],
        ),
    ]
