# Generated by Django 4.0 on 2022-12-15 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_groups_alter_user_user_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="date_updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
