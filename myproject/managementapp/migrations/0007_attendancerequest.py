# Generated by Django 5.1.3 on 2024-11-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("managementapp", "0006_attendancenotice_member_generation"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceRequest",
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
                ("title", models.TextField(max_length=300)),
                ("writer", models.CharField(max_length=200)),
                ("request_date", models.DateTimeField()),
                ("request_type", models.CharField(max_length=30)),
                ("content", models.TextField()),
                ("files", models.FileField(upload_to="")),
                ("rdate", models.DateTimeField()),
                ("approval", models.BooleanField(default=False)),
            ],
        ),
    ]
