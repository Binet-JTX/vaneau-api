# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('background', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('hruid', models.CharField(max_length=254)),
                ('lastname', models.CharField(max_length=254)),
                ('firstname', models.CharField(max_length=254)),
                ('promo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('filename', models.CharField(max_length=254)),
                ('category', models.ForeignKey(to='vote.Category', related_name='videos')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('category', models.ForeignKey(to='vote.Category', related_name='votes')),
                ('student', models.ForeignKey(to='vote.Student', related_name='votes')),
                ('video', models.ForeignKey(to='vote.Video', related_name='votes')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('student', 'category')]),
        ),
    ]
