# Generated by Django 4.1.4 on 2023-05-15 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0013_client_intervention'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='Intervention',
            new_name='Interventions',
        ),
    ]
