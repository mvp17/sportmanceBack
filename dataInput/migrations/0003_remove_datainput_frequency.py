# Generated by Django 4.2.5 on 2023-10-28 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dataInput", "0002_rename_datafile_datainput"),
    ]

    operations = [
        migrations.RemoveField(model_name="datainput", name="frequency",),
    ]