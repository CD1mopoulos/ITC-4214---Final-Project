# Generated by Django 5.1.3 on 2024-12-02 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games_db", "0002_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="stars",
            field=models.IntegerField(
                choices=[
                    (1, "1 Star"),
                    (2, "2 Stars"),
                    (3, "3 Stars"),
                    (4, "4 Stars"),
                    (5, "5 Stars"),
                ]
            ),
        ),
    ]
