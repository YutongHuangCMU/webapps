# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_auto_20161010_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='profile-photos/default.jpg', upload_to='profile-photos'),
        ),
    ]
