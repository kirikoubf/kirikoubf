# Generated by Django 4.1.4 on 2023-05-08 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0006_remove_produit_pointure_alter_produit_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]