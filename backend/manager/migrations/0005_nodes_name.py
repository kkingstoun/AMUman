# Generated by Django 5.0 on 2024-01-25 10:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0004_remove_nodes_is_active_nodes_last_seen_nodes_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="nodes",
            name="name",
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]