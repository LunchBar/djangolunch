# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 10:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20170206_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_member', to=settings.AUTH_USER_MODEL),
        ),
    ]