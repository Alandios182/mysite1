# Generated by Django 4.2.5 on 2023-10-04 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0005_delete_prueba_question_enabled_question_enabled_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="choice",
            name="suspended",
            field=models.BooleanField(default=False),
        ),
    ]
