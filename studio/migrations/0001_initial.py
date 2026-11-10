import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Master",
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
                ("name", models.CharField(max_length=100)),
                (
                    "specialization",
                    models.CharField(blank=True, max_length=100),
                ),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Design",
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
                ("title", models.CharField(max_length=150)),
                ("style", models.CharField(max_length=50)),
                ("price", models.PositiveIntegerField()),
                ("image_url", models.URLField()),
                (
                    "master",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="designs",
                        to="studio.master",
                    ),
                ),
            ],
            options={"ordering": ["id"]},
        ),
    ]
