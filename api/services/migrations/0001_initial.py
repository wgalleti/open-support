# Generated by Django 5.0.1 on 2024-01-16 17:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('description', models.CharField(max_length=100)),
                ('erp_code', models.IntegerField(blank=True, null=True)),
                ('logged_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_logged_user', to=settings.AUTH_USER_MODEL, verbose_name='user in logged')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('date', models.DateField()),
                ('closure_date', models.DateField(blank=True, null=True)),
                ('cancellation_date', models.DateField(blank=True, null=True)),
                ('cancellation_description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Started'), (2, 'Running'), (3, 'Finished'), (9, 'Canceled')], default=1)),
                ('description', models.TextField()),
                ('observation', models.TextField(blank=True, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True)),
                ('integration_create', models.BooleanField(blank=True, default=True, null=True)),
                ('cancellation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_cancellation', to=settings.AUTH_USER_MODEL)),
                ('closure_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_closure', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.customer')),
                ('logged_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_logged_user', to=settings.AUTH_USER_MODEL, verbose_name='user in logged')),
            ],
            options={
                'verbose_name': 'Service Order',
                'verbose_name_plural': 'Services Orders',
            },
        ),
        migrations.CreateModel(
            name='ServiceOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('duration', models.IntegerField(blank=True, default=1, null=True)),
                ('description', models.TextField()),
                ('logged_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_logged_user', to=settings.AUTH_USER_MODEL, verbose_name='user in logged')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('service_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.serviceorder')),
            ],
            options={
                'verbose_name': 'Service Order Item',
                'verbose_name_plural': 'Items of Services Orders',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('description', models.CharField(max_length=100)),
                ('value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('logged_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_logged_user', to=settings.AUTH_USER_MODEL, verbose_name='user in logged')),
            ],
            options={
                'verbose_name': 'Service Type',
                'verbose_name_plural': 'Types of Services',
            },
        ),
        migrations.CreateModel(
            name='ServiceOrderTech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('duration', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('logged_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_logged_user', to=settings.AUTH_USER_MODEL, verbose_name='user in logged')),
                ('service_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.serviceorder')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.attendant')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='services.servicetype')),
            ],
            options={
                'verbose_name': 'Service Order Tech',
                'verbose_name_plural': 'Techs of Services Orders',
            },
        ),
    ]