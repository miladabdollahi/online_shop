# Generated by Django 3.0.8 on 2020-09-20 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='title of comment')),
                ('positive_points', models.CharField(blank=True, max_length=250, verbose_name='positive points')),
                ('negative_points', models.CharField(blank=True, max_length=250, verbose_name='negative points')),
                ('text', models.TextField(verbose_name='text of comment')),
                ('status', models.CharField(choices=[('a', 'accepted'), ('w', 'awaiting approval'), ('n', 'not approved')], default='w', max_length=1, verbose_name='status of comment')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
    ]
