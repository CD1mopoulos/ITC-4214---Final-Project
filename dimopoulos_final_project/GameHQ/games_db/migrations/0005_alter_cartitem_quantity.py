# Generated by Django 5.1.3 on 2024-12-03 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games_db", "0004_purchase_completed_purchase_purchase_details_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
