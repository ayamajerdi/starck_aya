# Generated by Django 5.1.6 on 2025-05-21 00:04

import historique.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exportation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('fichier', models.FileField(upload_to=historique.models.chemin_export)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
