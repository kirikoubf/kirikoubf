# Generated by Django 4.1.4 on 2023-05-05 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('Name', models.CharField(max_length=25)),
                ('Description', models.TextField()),
                ('Quantite', models.IntegerField()),
                ('Pointure', models.IntegerField()),
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Image', models.ImageField(blank=True, upload_to='media')),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Factures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=25)),
                ('Prenom', models.TextField()),
                ('Telephone', models.CharField(max_length=8)),
                ('Pointure', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('Produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Produits', to='Gestion.produits')),
            ],
        ),
        migrations.CreateModel(
            name='Approvision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fournisseur', models.CharField(max_length=25)),
                ('Telephone', models.CharField(max_length=8)),
                ('Pointure', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('Produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Approvision', to='Gestion.produits')),
            ],
        ),
    ]