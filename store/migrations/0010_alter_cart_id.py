# Generated by Django 5.1.1 on 2024-09-06 19:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_rename_data_review_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]