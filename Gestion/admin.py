from .models import Produit
from django.contrib import admin
from .models import Produit, Facture, Approvision, Client, Commandes, Depense, DepensePrivee
# Register your models here.

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Description', 'Prix', 'Quantite', 'Id', 'Image', 'date_added')

class CommandesAdmin(admin.ModelAdmin):
    list_display = ('No', 'Nom', 'Prenom', 'Telephone', 'Produit', 'Quantite', 'Montant', 'Rabais', 'Total', 'Lieu', 'Statut', 'Payer', 'date_et_heure')

class FactureAdmin(admin.ModelAdmin):
    list_display = ('No', 'Nom', 'Prenom', 'Telephone', 'Produit', 'Quantite', 'Montant', 'Rabais', 'Total', 'Lieu','Livreur', 'date_et_heure')

class ApprovisionAdmin(admin.ModelAdmin):
    list_display = ('Fournisseur', 'Telephone', 'Produit','Quantite', 'date_added')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'Prenom', 'Telephone','Achats', 'Interventions', 'date_added')

class DepenseAdmin(admin.ModelAdmin):
    list_display = ('Motif', 'Montant', 'date_added')

class DepensePriveeAdmin(admin.ModelAdmin):
    list_display = ('Motif', 'Montant', 'date_added')

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(Approvision, ApprovisionAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Commandes, CommandesAdmin)
admin.site.register(Depense, DepenseAdmin)
admin.site.register(DepensePrivee, DepensePriveeAdmin)