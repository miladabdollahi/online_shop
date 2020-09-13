# Generated by Django 3.0.8 on 2020-09-12 08:42

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
                ('national_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد ملی')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('job', models.CharField(blank=True, max_length=150, null=True, verbose_name='شغل')),
                ('bank_card', models.IntegerField(blank=True, null=True, verbose_name='شماره کارت بانکی')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
