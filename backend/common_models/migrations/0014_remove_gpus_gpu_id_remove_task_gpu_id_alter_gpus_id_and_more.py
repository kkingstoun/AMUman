# Generated by Django 4.2.9 on 2024-01-27 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common_models", "0013_task_gpu_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gpus",
            name="gpu_id",
        ),
        migrations.RemoveField(
            model_name="task",
            name="gpu_id",
        ),
        migrations.AlterField(
            model_name="gpus",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]