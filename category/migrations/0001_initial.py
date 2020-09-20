# Generated by Django 3.0.8 on 2020-09-15 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('specification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name of category')),
                ('parent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='category.Category')),
                ('specification', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to='specification.Specification')),
            ],
        ),
    ]
