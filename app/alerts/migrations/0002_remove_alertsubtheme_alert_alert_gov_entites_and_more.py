# Generated by Django 4.0.3 on 2022-05-11 14:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alerts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alertsubtheme",
            name="alert",
        ),
        migrations.AddField(
            model_name="alert",
            name="gov_entites",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="alert",
            name="sub_themes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.DeleteModel(
            name="AlertGovEntity",
        ),
        migrations.DeleteModel(
            name="AlertSubTheme",
        ),
    ]
