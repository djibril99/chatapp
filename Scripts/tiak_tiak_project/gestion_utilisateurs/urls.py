from django.urls import path
from . import views
app_name = 'gestion_utilisateurs'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    #la liste des livreurs
    path('liste_livreurs/', views.liste_livreurs, name='liste_livreurs'),
    #profil d un utilisateur
    path('my_profil/', views.my_profil, name='my_profil'),
    #mettre a jour la position d un livreur
    path('update_position/', views.update_position, name='update_position'),
    #############################"" admin
    #liste des utilisateurs
    path('liste_clients/', views.liste_clients, name='liste_clients'),
    path('liste_livreurs_admin/', views.liste_livreurs_admin, name='liste_livreurs_admin'),
    path('demandes_d_acces_livreurs/', views.demandes_d_acces_livreurs, name='demandes_d_acces_livreurs'),
    path('recherche_utilisateur/', views.recherche_utilisateur, name='recherche_utilisateur'),
    path('changer_etat_livreur/id=<int:id>', views.changer_etat_livreur, name='changer_etat_livreur'),
    path('detail_utilisateur/id=<int:id>', views.detail_utilisateur, name='detail_utilisateur'),
    path('update_utilisateur/id=<int:id_utilisateur>', views.update_utilisateur, name='update_utilisateur'),
]
