# Generated by Django 5.0.1 on 2024-01-16 17:36

import django.db.models.deletion
import tickets.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        ("services", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
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
                (
                    "file",
                    models.FileField(upload_to=tickets.models.user_directory_path),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="update at"),
                ),
                ("started_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                (
                    "priority",
                    models.CharField(
                        choices=[("NORMAL", "Normal"), ("HIGH", "High")],
                        default="NORMAL",
                        max_length=50,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("STATED", "Started"),
                            ("WORKING", "Working"),
                            ("MORE_INFORMATION", "More Information"),
                            ("WAITING_CUSTOMER", "Waiting Customer"),
                            ("NEXT_VERSION", "In the next version"),
                            ("SOLVED", "Solved"),
                            ("DEPLOYED", "Deployed"),
                        ],
                        default="STATED",
                        max_length=50,
                    ),
                ),
                (
                    "departament",
                    models.CharField(
                        choices=[
                            ("SUPPORT", "Support"),
                            ("COMMERCIAL", "Commercial"),
                            ("DEVELOPMENT", "Development"),
                            ("FINANCIAL", "Financial"),
                        ],
                        default="SUPPORT",
                        max_length=50,
                    ),
                ),
                ("version", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "level",
                    models.IntegerField(
                        choices=[(1, "Support 1"), (2, "Support 2"), (3, "Support 3")],
                        default=1,
                    ),
                ),
                (
                    "attendant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.attendant",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.customer"
                    ),
                ),
                ("files", models.ManyToManyField(blank=True, to="tickets.attachment")),
                (
                    "logged_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="%(app_label)s_%(class)s_logged_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user in logged",
                    ),
                ),
                (
                    "service_order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="services.serviceorder",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ticket",
                "verbose_name_plural": "Tickets",
            },
        ),
        migrations.CreateModel(
            name="TicketInteraction",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="update at"),
                ),
                ("date", models.DateTimeField(auto_now_add=True, null=True)),
                ("description", models.TextField()),
                ("is_internal", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("STATED", "Started"),
                            ("WORKING", "Working"),
                            ("MORE_INFORMATION", "More Information"),
                            ("WAITING_CUSTOMER", "Waiting Customer"),
                            ("NEXT_VERSION", "In the next version"),
                            ("SOLVED", "Solved"),
                            ("DEPLOYED", "Deployed"),
                        ],
                        default="WORKING",
                        max_length=50,
                    ),
                ),
                (
                    "departament",
                    models.CharField(
                        choices=[
                            ("SUPPORT", "Support"),
                            ("COMMERCIAL", "Commercial"),
                            ("DEVELOPMENT", "Development"),
                            ("FINANCIAL", "Financial"),
                        ],
                        default="SUPPORT",
                        max_length=50,
                    ),
                ),
                (
                    "attendant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.attendant",
                    ),
                ),
                ("files", models.ManyToManyField(blank=True, to="tickets.attachment")),
                (
                    "logged_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="%(app_label)s_%(class)s_logged_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user in logged",
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tickets.ticket"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ticket Interaction",
                "verbose_name_plural": "Interation of Tickets",
                "ordering": ("id",),
            },
        ),
    ]
