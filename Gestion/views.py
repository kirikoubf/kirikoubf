from django.shortcuts import render, redirect
from .models import Profile
from datetime import datetime
from django.db.models import Count
from django.contrib.auth import authenticate as login_user
from django.contrib.auth import get_user_model
from django.contrib.auth import login as _login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Commandes, Client, Produit, Depense, Approvision, Facture, DepensePrivee
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.db.models import F, ExpressionWrapper, DecimalField
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login

User = get_user_model()


def login(request):
    user = request.user

    if request.method == "GET":
        if user.is_authenticated:
            if user.is_superuser:
                return redirect('/acceuil')
            
            if user.groups.filter(name='livreur').exists():
                return redirect('/acceuil_liv')

            if user.groups.filter(name='gerant').exists():
                return redirect('/acceuil_vend')

        return render(request, 'gestion/login.html')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("fsdgkxsdfgxsdfkjnxfjnxiejdhsgj",username,"irujgsiohdihgwotgshorhg",password)
        print(password)

        connect_user = login_user(request=request, username=username, password=password)

        if not connect_user:
            return render(request, 'gestion/login.html')

        _login(request=request, user=User.objects.get(username=connect_user)) 

        if connect_user:
            if connect_user.is_superuser:
                return redirect('/acceuil')
            
            if connect_user.groups.filter(name='livreur').exists():
                return redirect('/acceuil_liv')

            if connect_user.groups.filter(name='gerant').exists():
                return redirect('/acceuil_vend')

        return render(request, 'gestion/login.html')

    return render(request, 'gestion/login.html')


@login_required(login_url   ='login')
def acceuil(request):
    if request.method == "GET":
        if request.user.is_superuser:
            return render(request, "gestion/acceuil.html")

@login_required(login_url='login')
def acceuil_livreur(request):
    if request.method == "GET":
        return render(request, "gestion/acceuil_liv.html")

@login_required(login_url='login')
def acceuil_vendeuse(request):
    if request.method == "GET":
        return render(request, "gestion/acceuil_vend.html")


def commande(request):
    user = request.user
    if(request.method == "GET"):
        commandes = Commandes.objects.all()
        context = {'commandes': commandes}
        return render (request, 'gestion/commandes.html', context=context)


def create_commande(request):
    if request.method == "GET":
        produits = Produit.objects.all()
        clients = Client.objects.all()
        users = User.objects.all()
        context = {"produits": produits, "clients": clients, 'users': users}
        return render(request, "gestion/create_commande.html", context=context)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite'))
        rabais = int(request.POST.get('rabais'))
        lieu = request.POST.get('lieu')
        payer = request.POST.get('payer')
        statut = request.POST.get('statut')
        livreur = request.POST.get('livreur')
        
        # Vérifier si le produit existe
        produit = Produit.objects.get(Id=produit_id)

        # Vérifier la quantité disponible
        if quantite <= produit.Quantite:
            if statut == 'non livre':
                # Mettre à jour la quantité du produit
                produit.Quantite -= quantite
                produit.save()

                # Calculer le montant de la commande
                montant = quantite * produit.Prix
                total = montant - rabais

                # Créer la commande
                commande = Commandes.objects.create(
                    Nom=nom,
                    Prenom=prenom,
                    Telephone=telephone,
                    Produit=produit,
                    Quantite=quantite,
                    Montant=montant,
                    Rabais = rabais,
                    Total= total,
                    Lieu=lieu,
                    Statut=statut,
                    Payer=payer,
                    Livreur=livreur
                )
                commande.save()

            elif statut == 'livre' and quantite <= produit.Quantite:
                produit.Quantite -= quantite
                produit.save()
                # Vérifier si le client existe
                try:
                    client = Client.objects.get(Telephone=telephone)
                    client.Achats += quantite
                    client.Interventions += 1
                    client.save()
                except Client.DoesNotExist:
                    client = Client.objects.create(
                        Nom=nom,
                        Prenom=prenom,
                        Telephone=telephone,
                        Achats=quantite,
                        Interventions=1
                    )
                    client.save()
        
                # Calculer le montant de la facture
                montant = quantite * produit.Prix
                total = montant - rabais

                # Créer la facture
                facture = Facture.objects.create(
                    Nom=nom,
                    Prenom=prenom,
                    Telephone=telephone,
                    Produit=produit,
                    Quantite=quantite,
                    Montant=montant,
                    Rabais = rabais,
                    Total = total,
                    Lieu=lieu,
                    Livreur=livreur
                )
                facture.save()
        else:
            return redirect('/insuf')

    return redirect('/commandes')

def insuf(request):
    user = request.user
    if(request.method=="GET"):
        return render(request, "gestion/insuf.html")


def mod_com(request, commande_id):
    if(request.method=="GET"):
        commande = Commandes.objects.get(pk=commande_id)
        users = User.objects.all()
        context = {'commande': commande, 'users': users}
        return render (request, 'gestion/mod_commande.html', context=context)

    commande = get_object_or_404(Commandes, pk=commande_id)
    
    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        statut = request.POST.get('statut')
        payer = request.POST.get('payer')
        livreur = request.POST.get('livreur')

        if statut == 'non livre':
            commande.Statut = statut
            commande.Telephone = telephone
            commande.Payer = payer
            commande.Livreur = livreur
            commande.save()

        elif statut == 'livre':
            # Vérifier si le client existe
            try:
                client = Client.objects.get(Telephone=telephone)
                client.Achats += commande.Quantite
                client.Interventions += 1
                client.save()
            except Client.DoesNotExist:
                client = Client.objects.create(
                    Nom=commande.Nom,
                    Prenom=commande.Prenom,
                    Telephone=commande.Telephone,
                    Achats=commande.Quantite,
                    Interventions=1
                )
                client.save()

            # Calculer le montant de la facture

            # Créer la facture
            facture = Facture.objects.create(
                Nom=commande.Nom,
                Prenom=commande.Prenom,
                Telephone=commande.Telephone,
                Produit=commande.Produit,
                Quantite=commande.Quantite,
                Montant=commande.Montant,
                Rabais=commande.Rabais,
                Total=commande.Total,
                Lieu=commande.Lieu,
                Livreur=commande.Livreur
            )
            facture.save()
            commande.delete()
        elif statut == 'Annule':
            # Mettre à jour la quantité du produit
            commande_annulee = get_object_or_404(Commandes, pk=commande_id)

    # Ajouter la quantité annulée à la quantité du produit
            produit = commande_annulee.Produit
            produit.Quantite += commande_annulee.Quantite
            produit.save()
            # Supprimer la commande
            commande_annulee.delete()

        return redirect('/')  # Remplacez 'page_commandes' par l'URL de la page où vous souhaitez rediriger après la modification
        
    return render(request, 'gestion/mod_commande.html', {'commande': commande})




def facture(request):
    if(request.method == "GET"):
        factures = Facture.objects.all()
        context = {"factures": factures}
        return render (request, 'gestion/factures.html', context=context)


def create_facture(request):
    user = request.user

    if request.method == "GET":
        produits = Produit.objects.all()
        clients = Client.objects.all()
        users = User.objects.all()
        context = {"produits": produits, "clients": clients, "users": users}
        return render(request, "gestion/create_facture.html", context=context)

def profil_facture(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)

    context = {
        'facture': facture,
    }

    return render(request, 'gestion/profil_facture.html', context=context)

"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite'))
        lieu = request.POST.get('lieu')
        livreur = request.POST.get('livreur')

        # Vérifier si le produit existe
        produit = Produit.objects.get(Id=produit_id)
        
        if produit.Quantite >= quantite:
            # Créer une facture
            facture = Facture(Nom=nom, Prenom=prenom, Telephone=telephone, Produit=produit, Quantite=quantite, Montant=produit.Prix * quantite, Lieu=lieu, Livreur=livreur )
            facture.save()

            # Mettre à jour la quantité de produit disponible
            produit.Quantite -= quantite
            produit.save()

            # Vérifier si le client existe déjà
            client = Client.objects.filter(Telephone=telephone).first()

            if client:
                # Le client existe déjà, mettre à jour les informations
                client.Achats += quantite
                client.Interventions += 1
                client.save()
            else:
                # Créer un nouvel objet Client
                client = Client(Nom=nom, Prenom=prenom, Telephone=telephone, Achats=quantite, Interventions=1 )
                client.save()

            return redirect('/factures')
        else: 
            return render (request, 'gestion/insuf.html')
"""



def produit(request):
    user = request.user

    if(request.method == "GET"):
        produits = Produit.objects.all()
        context= {"produits": produits}
        return render (request, "gestion/produit.html", context=context)
        
def create_produit(request):
    user = request.user

    if (request.method == "GET"):
        return render(request, "gestion/create_produit.html")
        
    if (request.method == "POST"):
        name = request.POST.get("name")
        description = request.POST.get("description")
        id = request.POST.get("id")
        prix = request.POST.get("prix")
        quantite = request.POST.get("quantite")
        image = request.FILES.get("image")
    
        produit = Produit.objects.create(Name=name, Description=description, Id=id, Prix=prix, Quantite=quantite, Image=image).save()

        return redirect('/produits')


"""def profil_produit(request):
    user = request.user
    if(request.method =="GET"):
        produits=Produit.objects.all()
        context={"produits":produit}
        return render(request, "gestion/profil_produit", context=context)
"""

def profil_produit(request, produit_id):
    if (request.method=="GET"):
        produit = get_object_or_404(Produit, Id=produit_id)
        return render(request, 'gestion/profil_produit.html', {'produit': produit})





def clients(request):
    user = request.user
    if(request.method =="GET"):
        clients = Client.objects.all()
        context = {"clients": clients}
        return render(request, "gestion/clients.html", context=context)


def create_client(request):
    user = request.user

    if(request.method == "GET"):
        return render(request, "gestion/create_client.html")

    if(request.method == "POST"):
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        telephone = request.POST.get("telephone")
        achats = request.POST.get("achats")
        interventions = request.POST.get("interventions")
    
    client = Client.objects.create(Nom=nom, Prenom=prenom, Telephone=telephone, Achats=achats, Interventions=interventions).save()

    return redirect("/clients")




def depense(request):
    user = request.user

    if(request.method =="GET"):
        depenses = Depense.objects.all()
        context = {"depenses": depenses}
        return render(request, "gestion/depenses.html", context=context)


def create_depense(request):
    user = request.user
    
    if (request.method =="GET"):
        return render (request, "gestion/create_depense.html")
    
    if(request.method == "POST"):
        motif = request.POST.get("motif")
        montant = request.POST.get("montant")
    depense = Depense.objects.create(Motif=motif, Montant=montant).save()

    return redirect('/depenses')




def approvision(request):
    user = request.user

    if(request.method == "GET"):
        approvisions = Approvision.objects.all()
        context = {"approvisions": approvisions}
        return render(request, "gestion/approvisions.html", context=context)


def create_approvision(request):
    user = request.user
    if request.method == "GET":
        produits = Produit.objects.all()
        context = {"produits": produits}
        return render(request, "gestion/create_approvision.html", context=context)
    elif request.method == "POST":
        fournisseur = request.POST.get("fournisseur")
        telephone = request.POST.get("telephone")
        produit_id = request.POST.get("produit")
        quantite = int(request.POST.get("quantite"))
        montant = int(request.POST.get("montant"))

        produit = Produit.objects.get(Id=produit_id)

        approvision = Approvision.objects.create(Fournisseur=fournisseur, Telephone=telephone, Produit=produit, Quantite=quantite, Montant=montant)

    #   Mettre à jour la quantité du produit correspondant
    #   produit.Quantite += quantite
    #   produit.save()

        return redirect("/")




def depensesprivees(request):
    user = request.user
    if (request.method == "GET"):
        depensesprivees = DepensePrivee.objects.all()
        context={"depensesprivees": depensesprivees}
        return render (request, 'gestion/depensesprivees.html', context=context)


def create_depenseprivee(request):
    user = request.user
    
    if (request.method =="GET"):
        return render (request, "gestion/create_depenseprivee.html")
    
    if(request.method == "POST"):
        motif = request.POST.get("motif")
        montant = request.POST.get("montant")
    depenseprivee = DepensePrivee.objects.create(Motif=motif, Montant=montant).save()

    return redirect('/dep_priv')




def statistique(request):
    if (request.method == "GET"):
        produits=Produit.objects.all()
        products = Produit.objects.annotate(
        total_quantity=Sum('factures__Quantite'),
        total_amount=Sum(F('factures__Quantite') * F('factures__Produit__Prix')),
        month=TruncMonth('factures__date_et_heure')
    ).values('Id','Name', 'month', 'total_quantity', 'total_amount').order_by('month')

    return render(request, 'gestion/products_sold.html', {'products': products, "produits":produit})


def users(request):
    user = request.user
    if (request.method =="GET"):
        users = User.objects.all()
        context = {"users": users}
        return render(request, "gestion/users.html", context=context)
    
from django.contrib.auth.models import Group

def create_user(request):
    if request.method == "GET":
        users = User.objects.all()
        context = {"users": users}
        return render(request, "gestion/create_user.html", context=context)

    if request.method == "POST":
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone1 = request.POST.get('telephone1')
        telephone2 = request.POST.get('telephone2')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        statut = request.POST.get('statut')

        try:
            existing_user = User.objects.get(username=username)
            return render(request, 'create_user.html', {'error': 'Nom d\'utilisateur déjà utilisé'})
        except User.DoesNotExist:
            if statut == 'admin':
                user = User.objects.create_superuser(username=username, password=password, email=email, first_name=prenom, last_name=nom)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=prenom, last_name=nom)

            profile = Profile.objects.create(user=user, telephone1=telephone1, telephone2=telephone2, statut=statut)

            # Assigner l'utilisateur au groupe correspondant
            if statut == 'livreur':
                group = Group.objects.get(name='livreur')
            elif statut == 'gerant':
                group = Group.objects.get(name='gerant')
            else:
                group = None

        return redirect('/')

    return render(request, 'insuffisant.html')