# Generated by Django 4.1.4 on 2023-05-06 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0003_client_approvision_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='Id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]