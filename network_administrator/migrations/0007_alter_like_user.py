# Generated by Django 5.0.7 on 2024-12-24 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network_administrator", "0006_remove_like_session_key_like_session_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
