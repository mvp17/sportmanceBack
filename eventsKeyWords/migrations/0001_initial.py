# Generated by Django 4.2.5 on 2023-10-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KeyWordEventsFile",
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
                ("time_ms_name", models.CharField(max_length=50)),
                ("duration_time_ms_name", models.CharField(max_length=50)),
                ("chart_perf_vars", models.TextField(max_length=250)),
            ],
            options={"abstract": False,},
        ),
    ]
