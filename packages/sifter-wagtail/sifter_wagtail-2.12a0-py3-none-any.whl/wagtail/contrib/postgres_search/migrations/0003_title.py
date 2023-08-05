# Generated by Django 3.0.6 on 2020-04-24 13:00

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postgres_search', '0002_add_autocomplete'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexentry',
            name='title',
            field=django.contrib.postgres.search.SearchVectorField(default=''),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='indexentry',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='postgres_se_title_b56f33_gin'),
        ),
        migrations.AddField(
            model_name='indexentry',
            name='title_norm',
            field=models.FloatField(default=1.0),
        ),
    ]
