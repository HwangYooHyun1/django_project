# Generated by Django 5.1.3 on 2024-11-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("managementapp", "0005_alter_comments_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceNotice",
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
                ("content", models.TextField()),
                ("rdate", models.DateTimeField()),
                ("udate", models.DateTimeField()),
                ("view_count", models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name="member",
            name="generation",
            field=models.CharField(max_length=100, null=True),
        ),
    ]