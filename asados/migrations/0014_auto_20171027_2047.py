# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 20:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asados', '0013_remove_asado_estimated_cost'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DrinkSupply',
        ),
        migrations.DeleteModel(
            name='FoodSupply',
        ),
    ]
