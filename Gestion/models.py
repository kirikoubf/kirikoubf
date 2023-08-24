from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model

User = get_user_model()

class Produit(models.Model):
    Name = models.CharField(max_length=15)
    Description = models.TextField()
    Prix = models.IntegerField(default=8500)
    Quantite = models.IntegerField(default=0)
    Id = models.CharField(max_length=30, primary_key=True)
#    Pointure = models.IntegerField(default=45)
#    Couleur = models.CharField(max_length=15, default="Rouge")
    Image = models.ImageField(upload_to= 'media', blank=True)
    date_added = models.DateTimeField(auto_now=True)

    #def get_total_quantity_sold_per_month(self):
     #   return self.facture_set.annotate(month=TruncMonth('date_et_heure')).values('month').annotate(total_quantity=Sum('quantite')).order_by('month')

    def __str__(self) -> str:
        return f"{self.Id}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Produit")
        verbose_name_plurial = ("Produits")


class Commandes(models.Model):
    No = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=25)
    Prenom = models.TextField()
    Telephone = models.CharField(max_length=8)
    Produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    Quantite = models.IntegerField(default=1)
    Montant = models.IntegerField(default=1)
    Rabais = models.IntegerField(default=0)
    Total = models.IntegerField(default=0)
    Lieu = models.TextField(default="Boutique")
    STATUT_CHOICES = [
        ("non livre", "Non livré"),
        ("livre", "Livre"),
        ("Annule", "Annule")
    ]
    Statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="non livre")

    PAYER_CHOICES = [
        ("oui", "OUI"),
        ("non", "NON"),
    ]

    Payer = models.CharField(max_length=10, choices=PAYER_CHOICES, default="NON")


    Livreur = models.CharField(max_length=10, default="En cours")
    date_et_heure = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Nom}"

    class Meta:
        ordering = ['-date_et_heure']
        verbose_name = _("Commande")
        verbose_name_plural = "Commandes"



class Facture(models.Model):
    No = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=25)
    Prenom = models.TextField()
    Telephone = models.CharField(max_length=8)
    Produit = models.ForeignKey(Produit, related_name='factures', on_delete=models.CASCADE)
    Quantite = models.IntegerField(default=1)
    Montant = models.IntegerField(default=1)
    Rabais = models.IntegerField(default=0)
    Total = models.IntegerField(default=0)
    Lieu = models.TextField(default="Boutique")

    Livreur = models.CharField(max_length=10, default="Boutique")
    date_et_heure = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Nom}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Facture")
        verbose_name_plural = ("Factures")


class Approvision(models.Model):
    Fournisseur = models.CharField(max_length=25)
    Telephone = models.CharField(max_length=8)
    Produit = models.ForeignKey(Produit, related_name= 'Approvision', on_delete= models.CASCADE)
    Quantite = models.IntegerField(default=1)
    Montant = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Produit}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Facture")
        verbose_name_plurial = ("Factures")

    def save(self, *args, **kwargs):
        produit = self.Produit
        produit.Quantite += self.Quantite
        produit.save()
        super(Approvision, self).save(*args, **kwargs)


class Client(models.Model):
    Nom = models.CharField(max_length=25)
    Prenom = models.TextField()
    Telephone = models.CharField(max_length=8)
    Achats = models.IntegerField(default=1)
    Interventions = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Nom}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Client")
        verbose_name_plurial = ("Clients")


class Depense(models.Model):
    Motif = models.TextField()
    Montant = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Motif}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Depense")
        verbose_name_plurial = ("Depenses")
        

class DepensePrivee(models.Model):
    Motif = models.TextField()
    Montant = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Motif}"

    class meta:
        ordering = ['-date_added']
        verbose_name = ("Depense Privee")
        verbose_name_plurial = ("Depenses Privees")
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone1 = models.CharField(max_length=100)
    telephone2 = models.CharField(max_length=100)
    statut = models.CharField(max_length=100)

    # Autres champs de profil personnalisés

    def __str__(self):
        return self.user.username