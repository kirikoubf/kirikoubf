from django.shortcuts import render, redirect
from .models import Profile
from datetime import datetime
from datetime import datetime, time
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
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO

from django.core.mail import send_mail
from django.conf import settings

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

@login_required(login_url='login')
def commande(request):
    user = request.user
    if(request.method == "GET"):
        commandes = Commandes.objects.all()
        context = {'commandes': commandes}
        return render (request, 'gestion/commandes.html', context=context)
@login_required(login_url='login')
def commande_liv(request):
    user = request.user
    if(request.method == "GET"):
        commandes = Commandes.objects.all()
        context = {'commandes': commandes}
        return render (request, 'gestion/commandes_liv.html', context=context)

@login_required(login_url='login')
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
        equipe = request.POST.get('equipe')
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
                    Equipe=equipe,
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
                    Equipe=equipe,
                    Livreur=livreur
                )
                facture.save()
        else:
            return redirect('/insuf')

    return redirect('/commandes')


@login_required(login_url='login')
def insuf(request):
    user = request.user
    if(request.method=="GET"):
        return render(request, "gestion/insuf.html")

@login_required(login_url='login')
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
        equipe = request.POST.get('equipe')
        livreur = request.POST.get('livreur')

        commande.Statut = statut
        commande.Telephone = telephone
        commande.Payer = payer
        commande.Equipe = equipe
        commande.Livreur = livreur
        commande.save()

        if statut == 'livre':
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
                Equipe=equipe,
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



@login_required(login_url='login')
def facture(request):
    if(request.method == "GET"):
        factures = reversed(Facture.objects.all())
        context = {"factures": factures}
        return render (request, 'gestion/factures.html', context=context)

def profil_facture(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)

    context = {
        'facture': facture,
    }

    return render(request, 'gestion/profil_facture.html', context=context)


    return render(request, 'gestion/profil_facture.html', context=context)

@login_required(login_url='login')
def create_facture(request):
    user = request.user

    if request.method == "GET":
        produits = Produit.objects.all()
        clients = Client.objects.all()
        users = User.objects.all()
        context = {"produits": produits, "clients": clients, "users": users}
        return render(request, "gestion/create_facture.html", context=context)
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


@login_required(login_url='login')
def produit(request):
    user = request.user

    if(request.method == "GET"):
        produits = Produit.objects.all()
        produits_tries = sorted(produits, key=lambda produit: produit.Quantite, reverse=True)        
        context= {"produits": produits_tries}
        return render (request, "gestion/produit.html", context=context)

@login_required(login_url='login')        
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
@login_required(login_url='login')
def profil_produit(request, produit_id):
    if (request.method=="GET"):
        produit = get_object_or_404(Produit, Id=produit_id)
        return render(request, 'gestion/profil_produit.html', {'produit': produit})




@login_required(login_url='login')
def clients(request):
    user = request.user
    if(request.method =="GET"):
        clients = Client.objects.all()
        clients_tries = sorted(clients, key=lambda client: client.Achats, reverse=True)
        context = {"clients": clients_tries}
        return render(request, "gestion/clients.html", context=context)


@login_required(login_url='login')
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

def profil_client(request, client_id):
    if request.method =="GET":
        client = Client.objects.get(pk=client_id)
        factures = Facture.objects.filter(Telephone=client.Telephone)
        context = {'client': client, 'factures': factures}
        return render(request, 'gestion/profil_client.html', context=context)


@login_required(login_url='login')
def depense(request):
    user = request.user

    if(request.method =="GET"):
        depenses = Depense.objects.all()
        context = {"depenses": depenses}
        return render(request, "gestion/depenses.html", context=context)

@login_required(login_url='login')
def create_depense(request):
    user = request.user
    
    if (request.method =="GET"):
        return render (request, "gestion/create_depense.html")
    
    if(request.method == "POST"):
        motif = request.POST.get("motif")
        montant = request.POST.get("montant")
    depense = Depense.objects.create(Motif=motif, Montant=montant).save()

    return redirect('/depenses')



@login_required(login_url='login')
def approvision(request):
    user = request.user

    if(request.method == "GET"):
        approvisions = Approvision.objects.all()
        context = {"approvisions": approvisions}
        return render(request, "gestion/approvisions.html", context=context)

@login_required(login_url='login')
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



@login_required(login_url='login')
def depensesprivees(request):
    user = request.user
    if (request.method == "GET"):
        depensesprivees = DepensePrivee.objects.all()
        context={"depensesprivees": depensesprivees}
        return render (request, 'gestion/depensesprivees.html', context=context)

@login_required(login_url='login')
def create_depenseprivee(request):
    user = request.user
    
    if (request.method =="GET"):
        return render (request, "gestion/create_depenseprivee.html")
    
    if(request.method == "POST"):
        motif = request.POST.get("motif")
        montant = request.POST.get("montant")
    depenseprivee = DepensePrivee.objects.create(Motif=motif, Montant=montant).save()

    return redirect('/dep_priv')



@login_required(login_url='login')
def statistique(request):
    if (request.method == "GET"):
        produits=Produit.objects.all()
        products = Produit.objects.annotate(
        total_quantity=Sum('factures__Quantite'),
        total_amount=Sum(F('factures__Quantite') * F('factures__Produit__Prix')),
        total_total=Sum(F('factures__Total')),
        month=TruncMonth('factures__date_et_heure')
    ).values('Id','Name', 'month', 'total_quantity', 'total_amount', 'total_total').order_by('month')

    return render(request, 'gestion/products_sold.html', {'products': products, "produits":produit})

@login_required(login_url='login')
def users(request):
    user = request.user
    if (request.method =="GET"):
        users = User.objects.all()
        context = {"users": users}
        return render(request, "gestion/users.html", context=context)
    
from django.contrib.auth.models import Group
@login_required(login_url='login')
def create_user(request):
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
            user = User.objects.create_user(username=username, password=password, email=email, first_name=prenom, last_name=nom)

            profile = Profile.objects.create(user=user, telephone1=telephone1, telephone2=telephone2, statut=statut)

            # Assigner l'utilisateur au groupe correspondant
            if statut == 'livreur':
                group = Group.objects.get(name='livreur')
                user.groups.add(group)
            elif statut == 'gerant':
                group = Group.objects.get(name='gerant')
                user.groups.add(group)
            elif statut == 'superadmin':
                user.is_superuser = True
                user.is_staff = True  # Permet d'accéder à l'administration
                user.save()

            return redirect('/')  # Rediriger vers la page d'accueil

    return render(request, 'gestion/create_user.html')  # Afficher le formulaire de création d'utilisateur






def date(request):
    if request.method == "GET":
        return render(request, "gestion/form_somme.html")

    if request.method == "POST":
        jour = request.POST.get('jour')
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
        return redirect("sommes/", jour=jour, mois=mois, annee=annee)

def somme_factures(request):
    if request.method == "GET":
        jour_etudie = 28
        mois_etudie = 8
        annee_etudie = 2023

        sum_8_18 = Facture.objects.filter(
            date_et_heure__time__gte=time(8),
            date_et_heure__time__lt=time(18),
            date_et_heure__day=jour_etudie,
            date_et_heure__month=mois_etudie,
            date_et_heure__year=annee_etudie
        ).aggregate(Sum('Montant'))

        sum_18_23 = Facture.objects.filter(
            date_et_heure__time__gte=time(18),
            date_et_heure__time__lt=time(23),
            date_et_heure__day=jour_etudie,
            date_et_heure__month=mois_etudie,
            date_et_heure__year=annee_etudie
        ).aggregate(Sum('Montant'))

        return render(request, 'gestion/sommes.html', {
            'sum_8_18': sum_8_18['Montant__sum'],
            'sum_18_23': sum_18_23['Montant__sum'],
            'jour_etudie': jour_etudie,
            'mois_etudie': mois_etudie,
            'annee_etudie': annee_etudie,
        })



"""
def date(request):
    if request.method == "GET":
        return render(request, "gestion/form_somme.html")

    if request.method == "POST":
        jour = request.POST.get('jour')
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
        return redirect("sommes/", jour=jour, mois=mois, annee=annee)


def somme_factures(request, jour_etudie, mois_etudie, annee_etudie):
    jour_etudie = int(jour_etudie)
    mois_etudie = int(mois_etudie)
    annee_etudie = int(annee_etudie)

    time_ranges = [
        (time(8), time(18), 'sum_8_18'),
        (time(18), time(23), 'sum_18_23')
    ]

    sums = {}

    for start_time, end_time, sum_name in time_ranges:
        filtered_factures = Facture.objects.filter(
            date_et_heure__time__gte=start_time,
            date_et_heure__time__lt=end_time,
            date_et_heure__day=jour_etudie,
            date_et_heure__month=mois_etudie,
            date_et_heure__year=annee_etudie
        )
        total_amount = filtered_factures.aggregate(Sum('Montant'))
        sums[sum_name] = total_amount['Montant__sum']

    context = {
        'sums': sums,
        'jour_etudie': jour_etudie,
        'mois_etudie': mois_etudie,
        'annee_etudie': annee_etudie,
    }

    return render(request, 'gestion/sommes.html', context)
    """
"""
def generate_pdf(request, facture_id):
    # Récupérez les données de la facture depuis la base de données (Facture.objects.get...)
    facture = Facture.objects.get(pk=facture_id)

    # Récupérez le contenu HTML de la page de facture
    template = 'profil_facture.html'
    context = {'facture': facture}
    html_string = render(request, template, context).content.decode('utf-8')

    # Créez un objet WeasyPrint HTML à partir de la chaîne HTML
    html = HTML(string=html_string)

    # Créez un fichier temporaire pour le PDF
    pdf_file = BytesIO()

    # Générez le PDF et écrivez-le dans le fichier temporaire
    html.write_pdf(target=pdf_file)

    # Configurez la réponse HTTP pour le fichier PDF généré
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture_id}.pdf"'

    return response
"""



from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from django.template.loader import render_to_string  # Ajoutez cette ligne

def pdf(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)

    context = {
        'facture': facture,
    }

    # Générer le PDF à partir du modèle HTML
    html_string = render_to_string('gestion/pdf.html', context)
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)

    # Préparer la réponse HTTP pour le fichier PDF généré
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=facture_{facture_id}.pdf'
    response.write(pdf_file.getvalue())

    return response
"""
def compter(request):
    if request.method =="GET":
        factures = Facture.objects.all()
        context = {"factures": factures}
        return render (request, "gestion/compter.html", context=context)
"""

from django.shortcuts import render
from .models import Facture
from datetime import datetime, time

def compter(request):
    if request.method == "GET":
        # Récupérez la date à partir de la requête GET
        date_string = request.GET.get('date')
        
        if date_string is not None:
            try:
                # Convertissez la chaîne de date en objet datetime
                date = datetime.strptime(date_string, '%Y-%m-%d')
        
                # Obtenez la liste des équipes disponibles dans votre modèle Facture
                equipes = Facture.objects.values_list('Equipe', flat=True).distinct()
        
                # Créez des dictionnaires pour stocker les factures par équipe
                factures_par_equipe = {}
                
                # Créez des variables pour stocker les montants totaux par équipe
                montant_total_equipe01 = 0
                montant_total_equipe02 = 0
        
                # Pour chaque équipe, filtrez les factures par équipe et calculez le montant total
                for equipe in equipes:
                    factures_equipe = Facture.objects.filter(Equipe=equipe, date_et_heure__date=date)
                    montant_total_equipe = factures_equipe.aggregate(Sum('Total'))['Total__sum'] or 0
                    
                    # Stockez les factures dans le dictionnaire correspondant à l'équipe
                    factures_par_equipe[equipe] = factures_equipe
                    
                    # Stockez les montants totaux dans les variables appropriées
                    if equipe == 'equipe01':
                        montant_total_equipe01 = montant_total_equipe
                    elif equipe == 'equipe02':
                        montant_total_equipe02 = montant_total_equipe
        
                # Retournez les factures par équipe et les montants totaux dans un modèle HTML
                return render(request, 'gestion/compter.html', {
                    'date': date,
                    'factures_par_equipe': factures_par_equipe,
                    'montant_total_equipe01': montant_total_equipe01,
                    'montant_total_equipe02': montant_total_equipe02,
                })
            except ValueError:
                # La date saisie n'est pas au bon format
                return render(request, 'gestion/compter.html', {'erreur': 'Format de date incorrect'})
        else:
            # Aucune date saisie dans le formulaire
            return render(request, 'gestion/compter.html', {'erreur': 'Veuillez saisir une date'})

    return render(request, 'gestion/compter.html', {})



# views.py
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string

def reset_password(request):
    if request.method == "POST":
        # Récupérez l'adresse e-mail soumise dans le formulaire
        email = request.POST.get('email')

        try:
            # Vérifiez si un utilisateur avec cette adresse e-mail existe
            user = User.objects.get(email=email)

            # Générez un nouveau mot de passe temporaire
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Réinitialisez le mot de passe de l'utilisateur
            user.set_password(temp_password)
            user.save()

            # Envoyez un e-mail avec le nouveau mot de passe
            subject = 'Réinitialisation de votre mot de passe'
            message = f"Cher(e) {user.username},\n\nNous avons reçu une demande de réinitialisation de mot de passe pour votre compte.\n\nVotre nouveau mot de passe est : {temp_password} \n\nNous vous remercions de votre confiance en notre service.\nCordialement,\nL'équipe de support de Kirikoubf"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            # Affichez un message de succès
            messages.success(request, 'Un e-mail contenant le nouveau mot de passe a été envoyé à votre adresse.')

            # Redirigez l'utilisateur vers la page de connexion ou une autre page appropriée
            return redirect('confmail')  # Assurez-vous d'avoir une URL nommée 'login' dans vos URL

        except User.DoesNotExist:
            # Si l'utilisateur n'existe pas, affichez un message d'erreur
            messages.error(request, 'Aucun utilisateur avec cette adresse e-mail n\'a été trouvé.')

    return render(request, 'registration/password.html')

from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'registration/chpassword.html')

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        # Vérifiez si l'ancien mot de passe correspond
        user = authenticate(username=request.user.username, password=old_password)

        if user is not None:
            # Changez le mot de passe et sauvegardez l'utilisateur
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('confpass')  # Redirigez l'utilisateur vers la page d'accueil ou une autre page de votre choix
        else:
            messages.error(request, 'Mot de passe incorrect.')

    return render(request, 'registration/chpassword.html')

def confmail(request):
    if request.method == "GET":
        return render(request, 'registration/confmail.html')

def confpass(request):
    if request.method == "GET":
        return render(request, 'registration/confpass.html')
@login_required
def confcon(request):
    if request.method == "GET":
        return render(request, 'registration/confcon.html')
@login_required
def confdec(request):
    if request.method == "GET":
        return render(request, 'registration/confdec.html')

def error(request):
    if request.method == "GET":
        return render(request, 'registration/error.html')


@login_required
def redirection_accueil(request):
    if request.user.groups.filter(name='gerant').exists():
        return redirect('acceuil_vend')
    elif request.user.groups.filter(name='livreur').exists():
        return redirect('acceuil_liv')
    else:
        return redirect('acceuil')