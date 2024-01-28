# Generated by Django 4.2.9 on 2024-01-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("node", "0003_local_url"),
    ]

    operations = [
        migrations.RenameField(
            model_name="local",
            old_name="url",
            new_name="managerNmUrl",
        ),
        migrations.AddField(
            model_name="local",
            name="managerWsUrl",
            field=models.CharField(
                default="ws://localhost:8000/ws/node/", max_length=15
            ),
        ),
    ]
