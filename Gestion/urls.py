from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView
from .views import login, acceuil, acceuil_livreur, acceuil_vendeuse, create_commande, create_facture, create_produit, create_depense, create_client, create_approvision, clients, profil_client, depense, produit, approvision, commande, commande_liv, facture, mod_com, depensesprivees, create_depenseprivee, profil_produit, statistique, users, create_user, insuf, profil_facture
urlpatterns = [
    path('', login, name='login'),
    #path('login', login),
    path('cr_us', create_user, name="cr_us"),
    path('acceuil', acceuil, name="acceuil"),
    path('acceuil_liv', acceuil_livreur, name="acceuil_liv"),
    path('acceuil_vend', acceuil_vendeuse, name="acceuil_vend"),
    path('create_cm', create_commande, name='creer_commande'),
    path('create_prod', create_produit, name='creer_produit'),
    path('create_dep', create_depense, name='creer_depense'),
    path('create_cli', create_client, name='creer_client'),
    path('create_app', create_approvision, name='creer_approvision'),
    path('clients', clients, name='page_clients'),
    path('client/<int:client_id>/',profil_client, name='profil_client'),
    path('depenses', depense, name='page_depenses'),
    path('produits', produit, name='page_produits'),
    path('approvisions', approvision, name='page_approvisions'),
    path('commandes', commande, name='page_commandes'),
    path('commandes_liv', commande_liv, name='page_commandes_liv'),
    path('factures', facture, name='page_factures'),
    path('create_fact', create_facture, name='creer_facture'),
    #path('statistiques', stat_ventes, name='statistique'),
    path('dep_priv', depensesprivees, name='dep_priv'),
    path('create_dep_priv', create_depenseprivee, name='creer_depense_privee'),
    #path('mod_com', update_commande_statut)
    path('mod_com/<int:commande_id>', mod_com, name='modifier_commande'),
    path('stat', statistique, name='statistique'),
    #path('prof_prod/<str:produit_Id>', profil_produit, name="profil_produit")
    path('produit/<str:produit_id>/', profil_produit, name='profil_produit'),
    path('users', users, name="users"),
    path('create_user', create_user, name='create_user'),
    path('insuf', insuf, name='insuffissance'),
    path('facture/<int:facture_id>/', profil_facture, name='profil_facture'),
    path('date/', views.date, name='date'),
    path('sommes/', views.somme_factures, name='sommes'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('generate_pdf/<int:facture_id>/', views.pdf, name='generate_pdf'),
    path('compter', views.compter, name='compter'),
    # les email
    path('reset_password/', views.reset_password, name='reset_password'),
    #email
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change_password/', views.change_password, name='change_password'),
    path('confmail', views.confmail, name='confmail'),
    path('confpass', views.confpass, name='confpass'),
    path('confcon', views.confcon, name='confcon'),
    path('confdec', views.confdec, name='confdec'),
    path('ERROR', views.error, name='error'),
    path('redirection/', views.redirection_accueil, name='redirection_acceuil'),
    ]

