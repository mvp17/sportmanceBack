# Generated by Django 4.2.5 on 2023-10-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataInput", "0003_remove_datainput_frequency"),
    ]

    operations = [
        migrations.AddField(
            model_name="datainput",
            name="frequency",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
