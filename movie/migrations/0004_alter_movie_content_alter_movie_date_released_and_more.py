# Generated by Django 4.1.4 on 2022-12-08 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0003_rename_tag_movie_tag_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="content",
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name="movie",
            name="date_released",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name="movie",
            name="name",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="movie",
            name="official_site",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="movie",
            name="time",
            field=models.IntegerField(),
        ),
    ]
