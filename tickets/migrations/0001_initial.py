# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 23:48
from __future__ import unicode_literals

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
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('acc', 'Accepted'), ('asgn', 'ASSIGNED'), ('cls', 'CLOSED'), ('unasgn', 'UNASSIGNED')], default='unasgn', max_length=6)),
                ('goal', models.CharField(choices=[('en', 'ENHANCEMENT'), ('fx', 'FIX')], max_length=2)),
                ('priority', models.CharField(choices=[('hg', 'HIGH'), ('md', 'MEDIUM'), ('lw', 'LOW')], default='hg', max_length=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
