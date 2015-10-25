# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_video_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='rank',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
