# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-12 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0006_auto_20171212_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='story',
        ),
        migrations.AddField(
            model_name='story',
            name='associated_tools',
            field=models.ManyToManyField(related_name='associated_tools', to='tools.Tool'),
        ),
    ]