from django.shortcuts import redirect, render
from .models import Notification

from gestion_utilisateurs.models import Utilisateur, Livreur,Client
from gestion_commandes.models import Livraison
from gestion_messages.models import Message
from .models import Notification , Postulation

import math
#envoyer les donner instannemment au livreur 
from django.http import StreamingHttpResponse , HttpResponseRedirect
from django.db.models import Q

import time
import json

from gestion_utilisateurs.views import obtenir_adresse


#recuperer la liste des notifications dont la livraisons  se situe a un distance x de la position du livreur
def calculer_distance(lon1, lat1, lon2, lat2):
        try :
                R = 6371  # Rayon de la Terre, en kilomètres.
                # Convertir les latitudes et longitudes en radians.
                lat1 = math.radians(lat1)
                lon1 = math.radians(lon1)
                lat2 = math.radians(lat2)
                lon2 = math.radians(lon2)
                # Calcul de la distance en radians.
                d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))
                # Conversion de la distance en kilomètres.
                return d * R
        except Exception as e:
                return 0

def index(request):
        #verifier si l'utilisateur est connecter
        user_id = request.session.get('user_id')
        user = Utilisateur.objects.get(id=user_id) if user_id else None
        context={}
        if user :
                if user.type_utilisateur == 'livreur':
                       # recuperer la lister de livraison  a 20km de la position du livreur
                        livreur = Livreur.objects.get(user=user)
                        #recuperer les notifications dont la livraison n'a pas de livreur donc la livraison n'est pas encore affecter
                        notifications = Notification.objects.filter(postulation__livraison__livreur = None)
                        liste_notifications = []
                        distance_max = 20 #10km
                        for notification in notifications :
                                        #distance_valide = calculer_distance(livreur.longitude , livreur.latitude , notification.postulation.livraison.longitude_depart , notification.postulation.livraison.latitude_depart)           
                                        distance_livraison = calculer_distance(notification.livraison.longitude_arrivee , notification.livraison.latitude_arrivee , notification.livraison.longitude_depart , notification.livraison.latitude_depart)
                                        
                                        if -distance_max <= distance_livraison <= distance_max :
                                                #ajouter la notification dont la distance est inferieur a 20km a la liste des notifications
                                                data = (distance_livraison , notification)
                                                liste_notifications.append(data)
                        #renvoyer la liste des notifications
                        context = {'notifications' : liste_notifications,
                                   'livreur' : livreur,
                                   'utilisateur' : user
                                   } 
                        return render(request , 'gestion_notifications/liste_notification.html' , context)
        return render(request , 'gestion_utilisateurs/index.html')


def stream_response_generator(livreur:Livreur):
    initial_data = None
    while True:
                #recuperer la liste des livraisons dont la distance est inferieur a 10km dons les livreur de la livrasion sont null
                notifications = Notification.objects.filter()
                notifications = [ notification for notification in notifications if notification.livraison]
                
                livraions = [ notitfications.livraison for notitfications in notifications if notitfications.livraison.livreur == None ]
                valide_livraisons = 0
                for livraison in livraions :
                        if calculer_distance(livraison.longitude_depart , livraison.latitude_depart , livreur.longitude , livreur.latitude) < 10000 :
                                valide_livraisons+=1
                                
                #recuperer le nombre de conversation ayant un message non lu au moins
                messages = Message.objects.filter(destinataire=livreur.user , lu = False)
                nombre_messages_non_lu = len(messages)
                
                                
                #serialized_data = serializers.serialize('json', valide_livraisons)
        
                serialized_data = json.dumps({"livraion": valide_livraisons , "message":nombre_messages_non_lu})
                latest_data = serialized_data
                #latest_data = valide_livraisons

                # Comparez les données actuelles avec les précédentes pour éviter de renvoyer des données inutilement.
                if latest_data != initial_data:
                        initial_data = latest_data
                        yield f'data:{initial_data}\n\n'

                # Ajoutez une petite pause pour éviter une utilisation excessive des ressources.
                time.sleep(5)
                
def liste_notification_livreur_streaming(request):
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
        livreur = Livreur.objects.get(user=user)
        response =  StreamingHttpResponse(stream_response_generator(livreur),status=200, content_type='text/event-stream')
        response['Cache-Control']= 'no-cache',
        
        return response

#postuler pour une livraison en ligne // ajouer l utilisateur sue l liste dattente
def postuler_livraison(request , notification_id):
        user_id = request.session.get('user_id')
        user = Utilisateur.objects.get(id=user_id) if user_id else None
        if user :
                if user.type_utilisateur == 'livreur':
                        livreur = Livreur.objects.get(user=user)
                        notification = Notification.objects.get(id=notification_id)
                        notification.livreurs_postule.add(livreur)
                       
                        """mode postulation"""
                        prix_propose = 0
                        if request.method == 'POST':
                                prix_propose = request.POST.get('prix')
                        elif request.method == 'GET':
                                prix_propose = request.GET.get('prix')
                        
                        postulation  =  Postulation(livraison=notification.livraison , livreur=livreur , prixPropose= prix_propose)
                        postulation.save()
                        
                        notification.postulation.add(postulation)
                        """fin mode postulation"""
                        notification.save()
                        return redirect('gestion_notifications:index')
                        
        return redirect('gestion_notifications:index')

def annuler_postule(request , notification_id):
        user_id = request.session.get('user_id')
        user = Utilisateur.objects.get(id=user_id) if user_id else None
        if user :
                if user.type_utilisateur == 'livreur':
                        livreur = Livreur.objects.get(user=user)
                        notification = Notification.objects.get(id=notification_id)
                        
                        notification.livreurs_postule.remove(livreur)
                        postulation = Postulation.objects.filter(livraison=notification.livraison , livreur=livreur).first()
                        
                        notification.postulation.remove(postulation)
                        postulation.delete()
                        
                        notification.save()
                        return redirect('gestion_notifications:index')
                        
        return redirect('gestion_notifications:index')

def accepter_postule(request , notification_id):
        notification = Notification.objects.get(id=notification_id)
        if request.method == 'POST':
                livreur_id = request.POST.get('livreur_id')
                livreur = Livreur.objects.get(id = livreur_id)
                #marquer le livreur pour qu il ne puisse cumuler les missions
                livreur.on_mission = True
                livreur.save()
                #valider la postulation
                notification.postulation.livraison.livreur = livreur
                notification.postulation.livraison.save()
                notification.save()
        return redirect('gestion_commandes:mes_livraisons')

#administrateur
def liste_notification_admin(request,id_utilisateur):
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
        if utilisateur.type_utilisateur == 'livreur':
                livreur = Livreur.objects.get(user=utilisateur)
                notifications = Notification.objects.filter(Q(postulation__livraison__livreur = livreur) | Q(postulation__livreurs_postule=livreur))
        elif utilisateur.type_utilisateur == 'client':
                client = Client.objects.get(user=utilisateur)
                notifications = Notification.objects.filter(postulation__livraison__marchandise__client=client)
        liste_notifications = []
        for notification in notifications :
                livraison = notification.postulation.livraison
                if livraison :
                        distance = calculer_distance(livraison.longitude_depart , livraison.latitude_depart , livraison.longitude_arrivee , livraison.latitude_arrivee)
                        data = (distance , notification)
                        liste_notifications.append(data)

        context = {'notifications' : liste_notifications,
                        'utilisateur' : utilisateur
                        }
        return render(request , f'gestion_notifications/admin/{utilisateur.type_utilisateur}/liste_livraison.html' , context)
def supprimer(request, id_notification, id_utilisateur):
        notification = Notification.objects.get(id=id_notification)
        # Supprimer la livraison associée à la notification. la notification est supprimer automatiquement
        notification.postulation.livraison.delete()
        
        return liste_notification_admin(request, id_utilisateur)
#section pour  administrateur

def detail_notification(request, id_notification,id_utilisateur):
        try :
                notification = Notification.objects.get(id=id_notification)
                utilisateur = Utilisateur.objects.get(id=id_utilisateur)
                distance = calculer_distance(notification.livraison.longitude_depart , notification.livraison.latitude_depart , notification.livraison.longitude_arrivee , notification.livraison.latitude_arrivee)
                data = [(distance , notification)]
                context = {'notifications' : data,
                           'utilisateur' : utilisateur
                           }
                return render(request , f'gestion_notifications/admin/{utilisateur.type_utilisateur}/liste_livraison.html' , context)
        except Exception as e:
                print(e)
                return redirect('gestion_notifications:index')
      