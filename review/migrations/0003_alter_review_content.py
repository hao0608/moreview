# Generated by Django 4.1.4 on 2022-12-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0002_review_existed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
