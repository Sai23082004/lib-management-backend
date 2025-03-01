# Generated by Django 5.1 on 2025-02-28 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(blank=True, max_length=20, null=True)),
                ('firstName', models.CharField(blank=True, max_length=100)),
                ('lastName', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('branch', models.CharField(blank=True, max_length=50, null=True)),
                ('startyear', models.IntegerField(blank=True, null=True)),
                ('endyear', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BooksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=40, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('submited', models.BooleanField(default=False)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('submited_date', models.DateTimeField(blank=True, null=True)),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='library_books', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='users.usersmodel')),
            ],
        ),
    ]
