# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-06-15 21:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fault',
            name='correct_straight_times',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u8fde\u7eed\u7b54\u5bf9\u6b21\u6570'),
        ),
        migrations.AddField(
            model_name='fault',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u6709\u6548'),
        ),
        migrations.AddField(
            model_name='fault',
            name='question_type',
            field=models.PositiveSmallIntegerField(choices=[(1, '\u5355\u9009'), (2, '\u591a\u9009'), (3, '\u586b\u7a7a'), (4, '\u4e3b\u89c2')], db_index=True, default=4, verbose_name='\u7c7b\u522b'),
        ),
        migrations.AddField(
            model_name='paper',
            name='is_break_through',
            field=models.BooleanField(default=True, verbose_name='\u95ef\u5173'),
        ),
        migrations.AddField(
            model_name='paper',
            name='order_number',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='\u6309\u6570\u5b57\u4ece\u5c0f\u5230\u5927\u6392\u5e8f', verbose_name='\u5e8f\u53f7'),
        ),
        migrations.AddField(
            model_name='paper',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='corrected',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u8ba2\u6b63'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='faults', to='exam.Paper', verbose_name='\u8bd5\u5377'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='times',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u6b21\u6570'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exam_faults', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='owner_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='\u5f52\u7c7b'),
        ),
    ]
