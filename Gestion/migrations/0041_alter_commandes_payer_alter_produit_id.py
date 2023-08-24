# Generated by Django 4.1.4 on 2023-07-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0040_alter_commandes_livreur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandes',
            name='Payer',
            field=models.CharField(choices=[('oui', 'OUI'), ('non', 'NON')], default='NON', max_length=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='Id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
