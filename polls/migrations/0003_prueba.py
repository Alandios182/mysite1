# Generated by Django 4.2.5 on 2023-09-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0002_question_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prueba",
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
                ("nombre_text", models.CharField(max_length=200)),
            ],
        ),
    ]
