# Generated by Django 3.0.8 on 2020-09-20 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Costumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='national code')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('job', models.CharField(blank=True, max_length=150, null=True, verbose_name='job')),
                ('bank_card', models.IntegerField(blank=True, null=True, verbose_name='bank card number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'costumer',
                'verbose_name_plural': 'costumers',
            },
        ),
    ]