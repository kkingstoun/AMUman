# Generated by Django 4.2.9 on 2024-01-28 21:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common_models", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gpus",
            name="status",
            field=models.CharField(
                choices=[
                    ("Waiting", "Waiting"),
                    ("Running", "Running"),
                    ("Reserved", "Reserved"),
                    ("Unavailable", "Unavailable"),
                ],
                default="Waiting",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="nodes",
            name="status",
            field=models.CharField(
                choices=[
                    ("Waiting", "Waiting"),
                    ("Running", "Running"),
                    ("Reserved", "Reserved"),
                    ("Unavailable", "Unavailable"),
                ],
                default="Waiting",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("Waiting", "Waiting"),
                    ("Pending", "Pending"),
                    ("Running", "Running"),
                    ("Finished", "Finished"),
                    ("Interrupted", "Interrupted"),
                ],
                default="Waiting",
                max_length=50,
            ),
        ),
    ]
