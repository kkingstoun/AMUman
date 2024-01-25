# Generated by Django 4.2.9 on 2024-01-25 11:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("common_models", "0002_task_submit_time_task_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Nodes",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ip", models.CharField(max_length=15, unique=True)),
                (
                    "name",
                    models.CharField(blank=True, max_length=15, null=True, unique=True),
                ),
                ("port", models.IntegerField(blank=True, null=True)),
                ("gpu_info", models.TextField(blank=True, null=True)),
                ("status", models.CharField(default="free", max_length=10)),
                (
                    "last_seen",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Gpus",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("brand_name", models.TextField(blank=True, null=True)),
                ("gpu_speed", models.TextField(blank=True, null=True)),
                ("gpu_info", models.TextField(blank=True, null=True)),
                ("status", models.CharField(default="free", max_length=10)),
                (
                    "nodeid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common_models.nodes",
                    ),
                ),
            ],
        ),
    ]
