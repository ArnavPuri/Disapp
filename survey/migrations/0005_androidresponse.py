# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20161216_0449'),
    ]

    operations = [
        migrations.CreateModel(
            name='AndroidResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('response_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]