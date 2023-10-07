# Generated by Django 4.2.5 on 2023-10-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DataFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=100)),
                ("athlete", models.CharField(blank=True, max_length=100)),
                ("csv", models.FileField(upload_to="csv_files/")),
                ("is_event_file", models.BooleanField()),
                ("frequency", models.PositiveIntegerField()),
            ],
        ),
    ]
