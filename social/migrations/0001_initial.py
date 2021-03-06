# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-02-18 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='用户id')),
                ('uid2', models.IntegerField(verbose_name='用户id')),
            ],
            options={
                'db_table': 'friends',
            },
        ),
        migrations.CreateModel(
            name='Swiped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='用户自己')),
                ('sid', models.IntegerField(verbose_name='用户滑动过的人')),
                ('stype', models.CharField(choices=[('like', '滑动，喜欢'), ('superlike', '滑动，超级喜欢'), ('dislike', '滑动 不喜欢')], max_length=16, verbose_name='滑动的类型')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
            ],
            options={
                'db_table': 'swiped',
            },
        ),
        migrations.AlterUniqueTogether(
            name='swiped',
            unique_together=set([('uid', 'sid')]),
        ),
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together=set([('uid1', 'uid2')]),
        ),
    ]
