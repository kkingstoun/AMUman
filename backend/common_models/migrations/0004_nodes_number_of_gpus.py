# Generated by Django 4.2.9 on 2024-01-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common_models", "0003_nodes_gpus"),
    ]

    operations = [
        migrations.AddField(
            model_name="nodes",
            name="number_of_gpus",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
