# Generated by Django 2.2.5 on 2019-09-19 21:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190918_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='intern',
            name='is_accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='intern',
            name='is_reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(default='Development', max_length=200),
        ),
        migrations.AlterField(
            model_name='intern',
            name='job_title',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.Job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 20, 2, 42, 34, 907319), verbose_name='date published'),
        ),
    ]
