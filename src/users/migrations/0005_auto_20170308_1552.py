# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-08 15:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_is_leader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='order',
        ),
        migrations.RemoveField(
            model_name='user',
            name='order_note',
        ),
    ]
