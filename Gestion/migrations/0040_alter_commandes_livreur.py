# Generated by Django 4.1.4 on 2023-07-19 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0039_alter_facture_livreur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandes',
            name='Livreur',
            field=models.CharField(default='En cours', max_length=10),
        ),
    ]