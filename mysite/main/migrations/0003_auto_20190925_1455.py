# Generated by Django 2.2.4 on 2019-09-25 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190925_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intern',
            name='job_title',
        ),
        migrations.AlterField(
            model_name='job',
            name='job_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 25, 14, 55, 9, 630888), verbose_name='date published'),
        ),
    ]
