# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='token_password',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
