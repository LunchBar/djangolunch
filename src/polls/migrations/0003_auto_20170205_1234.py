# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_restaurant_is_ok'),
        ('polls', '0002_auto_20170201_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='NextweekRestaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nextweek', to='restaurants.Restaurant')),
            ],
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
