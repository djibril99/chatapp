from django.template import loader
# Create your views here.
from .models import Client, Livreur, Utilisateur, Admin
from gestion_notifications.models import Notification
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render, redirect
from geopy.geocoders import Nominatim
from .forms import InscriptionForm , ConnectionForm , UpdateProfil
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

#**************************************************
def index(request):
        #liste_clients = Client.objects.all()
        #liste_livreurs = Livreur.objects.all()
        
        #recuperer le template
        template = loader.get_template('gestion_utilisateurs/index.html')
        context = {}
        return HttpResponse(template.render(context, request))
        
        #return HttpResponse("Liste des clients : {} <br> Liste des livreurs : {}".format(clients, livreurs))
        #return HttpResponse("Hello, world. You're at the gestion_utilisateurs index.")
        
#**************************************************

def register(request):
        form = InscriptionForm()
        if request.method == 'POST':
                form = InscriptionForm(request.POST, request.FILES)
                print('valide : ', form.is_valid())
                if form.is_valid():
                        utilisateur = form.save()
                        messages.success(request, 'Inscription réussie. Vous pouvez maintenant vous connecter.')
                        # Redirigez l'utilisateur vers une page de confirmation ou d'accueil, par exemple.
                        return redirect('gestion_utilisateurs:index')

                else :
                        errors = form.errors
                        for error in errors:
                                print(error)
                        messages.error(request, 'Erreur lors de l\'inscription. Veuillez vérifier les champs.')

        return render(request, 'gestion_utilisateurs/index.html', {'form': form})
#connection d un utilisateur
def login(request):
        form = ConnectionForm()
        if request.method == 'POST':
                form = ConnectionForm(request.POST)
                if form.is_valid():
                        telephone = form.cleaned_data['telephone']
                        password = form.cleaned_data['password']
                        utilisateurs = Utilisateur.objects.filter(telephone=telephone, password=password)
                        utilisateur = utilisateurs.first() if utilisateurs.exists() else None
                        if utilisateur:
                                
                                
                                
                                
                                request.session['user_id'] = utilisateur.id
                                utilisateur.online = True
                                utilisateur.save()
                                #redirectionner vers la page appropriee
                                if utilisateur.type_utilisateur == 'client':
                                        return redirect('gestion_utilisateurs:liste_livreurs')

                                elif utilisateur.type_utilisateur == 'livreur':
                                        #verifier si le livreur est autoriser a se connecter
                                        livreur = Livreur.objects.get(user=utilisateur)
                                        if livreur.actif == False:
                                                messages.error(request, 'Votre compte n\'est pas encore actif. Veuillez revenir plus tard.')
                                                return redirect('gestion_utilisateurs:index')
                                        else:
                                                return redirect('gestion_commandes:mes_livraisons_livreur')

                                elif utilisateur.type_utilisateur == 'admin':
                                        #admin=Admin.objects.get(user=utilisateur)
                                        return redirect('gestion_utilisateurs:liste_clients')

                        else:
                                messages.error(request, 'Identifiants incorrects.')
                                
                                return redirect('gestion_utilisateurs:index')
                else:
                        messages.error(request, 'Identifiants incorrects.')
                        return redirect('gestion_utilisateurs:index')
        return render(request, 'gestion_utilisateurs/index.html', {'form': form})

#deconnection d un utilisateur
def logout(request):
        user_id = request.session['user_id']
        if user_id:
                utilisateur = Utilisateur.objects.get(id=user_id)
                utilisateur.online = False
                utilisateur.save()
                del request.session['user_id']
        return redirect('gestion_utilisateurs:index')

def my_profil(request):
    id_utilisateur = request.session.get('user_id')  # Utilisez get() pour éviter les erreurs si la clé 'user_id' n'existe pas
    errors = []
    success = []

    if not id_utilisateur:
        return redirect('gestion_utilisateurs:index')

    utilisateur = Utilisateur.objects.get(id=id_utilisateur)

    if request.method == 'POST':
        form = UpdateProfil(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save(user=utilisateur)  # Vous n'avez pas besoin de passer 'user=utilisateur' car le formulaire utilise déjà l'instance
            success.append('Modification réussie.')
        else:
            errors.extend(form.errors)

    context = {
        'utilisateur': utilisateur,
        'errors': errors,
        'success': success,
    }

    return render(request, f'gestion_utilisateurs/{utilisateur.type_utilisateur}/profil.html', context)

#la liste des livreurs depuis l application gestion_utilisateurs


def obtenir_adresse(latitude, longitude):
        try:
                geolocator = Nominatim(user_agent="myGeocoder")
                location = geolocator.reverse((latitude, longitude), language="fr")
                adresse = location.address if location else "Adresse non trouvée"
                return adresse
        except:
                return 'Introuvable'


def liste_livreurs(request):
    
        liste = []  # Utilisez un dictionnaire pour stocker les adresses par ID de livreur
        livreurs = []
        if request.method == 'POST':
                recherche = request.POST['recherche']
                livreurs = Livreur.objects.filter(Q(user__nom__icontains=recherche) | Q(user__prenom__icontains=recherche) | Q(user__telephone__icontains=recherche) | Q(user__email__icontains=recherche))
        else :
                livreurs = Livreur.objects.all()
                
        for livreur in livreurs:
                adresse = obtenir_adresse(livreur.latitude, livreur.longitude)        
                liste.append((livreur, adresse))
  

        context = {
                'liste_livreurs': liste,
                'recherche': True,
        }
                

        return render(request, 'gestion_utilisateurs/client/liste_livreurs.html', context)

#////////////////////////////////////'''''""""""""""""""""""""""""""""""""""#
#views pour les livreurs

@csrf_exempt
def update_position(request):
        user_id = request.session['user_id']
        if not user_id:
                return redirect('gestion_utilisateurs:index')
        utilisateur = Utilisateur.objects.get(id=user_id)
        if utilisateur.type_utilisateur == 'livreur':
                livreur = Livreur.objects.get(user=utilisateur)
                if request.method == 'POST':
                        # Récupérez les données de position depuis la requête POST
                        data = json.loads(request.body)
                        longitude = data.get('longitude')
                        latitude = data.get('latitude')

                        # Mettez à jour la position du livreur dans la base de données
                        livreur = Livreur.objects.get(id=1)  # Remplacez 1 par l'ID du livreur concerné
                        livreur.longitude = longitude
                        livreur.latitude = latitude
                        livreur.save()

                        # Répondez au client avec une réponse JSON (optionnel)
                        response_data = {'message': 'Position du livreur mise à jour avec succès'}
                        return JsonResponse(response_data)
                else:
                        # Gérez d'autres méthodes HTTP si nécessaire
                        return HttpResponse('Méthode HTTP non autorisée.', status=405)
                
#view pour l admin
def liste_clients(request):
        liste_clients = Client.objects.all()
        context = {
                'listes_utilisateurs': liste_clients,
                'page': 'clients'
        }
        return render(request, 'gestion_utilisateurs/admin/liste_utilisateur.html', context)
def liste_livreurs_admin(request):
        liste_livreurs = Livreur.objects.all()
        context = {
                'listes_utilisateurs': liste_livreurs,
                'page': 'livreurs'
        }
        return render(request, 'gestion_utilisateurs/admin/liste_utilisateur.html', context)
def demandes_d_acces_livreurs(request):
        liste_livreurs = Livreur.objects.filter(actif=False)
        context = {
                'listes_utilisateurs': liste_livreurs,
                'page': 'demandes_d_acces'
        }
        return render(request, 'gestion_utilisateurs/admin/liste_utilisateur.html', context)


def liste_livreur_desactive(request):
        liste_livreurs = Livreur.objects.filter(actif=False)
        context = {
                'listes_utilisateurs': liste_livreurs
        }
        return render(request, 'gestion_utilisateurs/admin/liste_utilisateur.html', context)   

def recherche_utilisateur(request):
        user = Utilisateur.objects.get(id=request.session['user_id'])
        context = {'recherche': True}
        if request.method == 'POST':
                recherche = request.POST['recherche']
                clients = Client.objects.filter(Q(user__nom__icontains=recherche) | Q(user__prenom__icontains=recherche) | Q(user__telephone__icontains=recherche) | Q(user__email__icontains=recherche))
                livreurs = Livreur.objects.filter(Q(user__nom__icontains=recherche) | Q(user__prenom__icontains=recherche) | Q(user__telephone__icontains=recherche) | Q(user__email__icontains=recherche))
                resultat = list(clients) + list(livreurs)
                if len(resultat) == 0:
                        context['listes_utilisateurs'] = resultat
                        
        if user.type_utilisateur == 'admin':
                return render(request, 'gestion_utilisateurs/admin/liste_utilisateur.html', context)
        else :
                return render(request, 'gestion_utilisateurs:index')
def changer_etat_livreur(request, id):
        livreur = Livreur.objects.get(id=id)
        if livreur.actif == False:
                livreur.actif = True
                livreur.save()
        else:
                livreur.actif = False
                livreur.save()
        return redirect('gestion_utilisateurs:liste_livreurs_admin')
def detail_utilisateur(request, id):
        utilisateur = Utilisateur.objects.get(id=id)
        #liste des livraions postuler et effecter pour les ivreur
        liste_Notifications = []
        if utilisateur.type_utilisateur == 'livreur':
                livreur = Livreur.objects.get(user=utilisateur)
                livraisons_postuler = Notification.objects.filter(livreurs_postule= livreur)
                livraisons_effectuer = Notification.objects.filter(postulation__livraison__livreur=livreur)
                liste_Notifications = list(livraisons_postuler) + list(livraisons_effectuer)
        #liste des livraisons poster par le client
        if utilisateur.type_utilisateur == 'client':
                client = Client.objects.get(user=utilisateur)
                livraisons_poster = Notification.objects.filter(postulation__livraison__marchandise__client=client)
                liste_Notifications = list(livraisons_poster)
                
        print(len(liste_Notifications))
        context = {
                'utilisateur': utilisateur,
                'liste_Notifications': liste_Notifications,
        }
        if utilisateur.type_utilisateur == 'livreur':
                context['livreur'] = Livreur.objects.get(user=utilisateur)
        
        return render(request, 'gestion_utilisateurs/admin/detail_utilisateur.html', context)

def update_utilisateur(request,id_utilisateur):

    if not id_utilisateur:
        return redirect('gestion_utilisateurs:index')

    utilisateur = Utilisateur.objects.get(id=id_utilisateur)

    if request.method == 'POST':
        form = UpdateProfil(request.POST, instance=utilisateur)
        if form.is_valid():
            utilisateur= form.save(user=utilisateur)  
            utilisateur.save()
        print('utilisateur : ', utilisateur)
    context = {
        'utilisateur': utilisateur,
    }

    return render(request, f'gestion_utilisateurs/admin/detail_utilisateur.html', context)