# Generated by Django 4.1.4 on 2023-05-08 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0005_remove_approvision_pointure_remove_facture_pointure_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='Pointure',
        ),
        migrations.AlterField(
            model_name='produit',
            name='Quantite',
            field=models.IntegerField(default=0),
        ),
    ]
