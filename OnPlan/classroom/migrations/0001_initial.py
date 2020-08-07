# Generated by Django 3.0.7 on 2020-08-07 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='tarefa_personalizada',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('titulo', models.CharField(max_length=400, unique=True)),
                ('materia', models.CharField(max_length=400, unique=True)),
                ('descricao', models.CharField(max_length=10000, unique=True)),
                ('classroom', models.CharField(max_length=50, unique=True)),
                ('data_limite', models.CharField(max_length=400, unique=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='tarefa_classroom',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('titulo', models.CharField(max_length=400, unique=True)),
                ('materia', models.CharField(max_length=400, unique=True)),
                ('descricao', models.CharField(max_length=10000, unique=True)),
                ('classroom', models.CharField(max_length=50, unique=True)),
                ('data_limite', models.CharField(max_length=400, unique=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
