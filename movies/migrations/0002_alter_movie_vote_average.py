# Generated by Django 4.2 on 2023-04-27 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="vote_average",
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]
