# Generated by Django 4.1.4 on 2023-05-05 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=25)),
                ('Prenom', models.TextField()),
                ('Telephone', models.CharField(max_length=8)),
                ('Pointure', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Produits',
            new_name='Produit',
        ),
        migrations.DeleteModel(
            name='Factures',
        ),
        migrations.AddField(
            model_name='facture',
            name='Produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Produit', to='Gestion.produit'),
        ),
    ]
