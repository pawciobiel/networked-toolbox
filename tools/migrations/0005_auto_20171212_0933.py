# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-12 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_auto_20171212_0843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='story',
        ),
        migrations.AddField(
            model_name='tool',
            name='story',
            field=models.ManyToManyField(null=True, related_name='associated_tools', to='tools.Story'),
        ),
    ]