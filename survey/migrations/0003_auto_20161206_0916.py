# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 03:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20161206_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerimage',
            name='answerbase_ptr',
        ),
        migrations.DeleteModel(
            name='AnswerImage',
        ),
    ]
