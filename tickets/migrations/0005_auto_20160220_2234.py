# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20160220_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='goal',
            field=models.CharField(choices=[('Enhancement', 'Enhancement'), ('Fix', 'Fix')], max_length=11),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='High', max_length=6),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(blank=True, choices=[('Accepted', 'Accepted'), ('Assigned', 'Assigned'), ('Closed', 'Closed'), ('Unassigned', 'Unassigned')], default='Unassigned', max_length=10),
        ),
    ]
