# Generated by Django 4.2.9 on 2024-01-25 16:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("common_models", "0007_gpus_gpu_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gpus",
            old_name="nodeid",
            new_name="node_id",
        ),
    ]