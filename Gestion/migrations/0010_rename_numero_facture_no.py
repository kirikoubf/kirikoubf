# Generated by Django 4.1.4 on 2023-05-08 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0009_rename_id_facture_numero'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facture',
            old_name='Numero',
            new_name='No',
        ),
    ]
