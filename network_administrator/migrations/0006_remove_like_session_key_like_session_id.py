# Generated by Django 5.0.7 on 2024-12-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network_administrator", "0005_like_session_key"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="like",
            name="session_key",
        ),
        migrations.AddField(
            model_name="like",
            name="session_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
