# Generated by Django 4.1.4 on 2023-05-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0020_facturetemporaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturetemporaire',
            name='Statut',
            field=models.CharField(choices=[('non livre', 'Non livré'), ('livre', 'Livre')], default='non livre', max_length=10),
        ),
    ]
