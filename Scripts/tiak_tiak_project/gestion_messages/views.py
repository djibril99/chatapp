from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import Message
from django.contrib.auth.decorators import login_required
from  gestion_utilisateurs.models import Utilisateur




def lire_message(request, user_id):
         # Récupérer toutes les conversations et afficher les messages de la dernière conversation
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
        
        user_conversation = Utilisateur.objects.get(id=user_id)
        messages = Message.objects.filter(Q(expediteur=user , destinataire=user_conversation) | Q(destinataire=user , expediteur=user_conversation)).order_by('date_envoi')
        #mmarquer comme lu les messages
        for message in messages:
                if message.destinataire == user :
                        message.lu = True
                        message.save()
             
        

        all_message= Message.objects.filter(Q(expediteur=user) | Q(destinataire=user)).order_by('date_envoi')
        all_converation = [ message.destinataire for message in all_message if message.expediteur == user ] + [ message.expediteur for message in all_message if message.destinataire == user ]

        #ajouter l utilisateur a la liste des conversation a l index 0
        all_converation.insert(0 , user_conversation)
        #affacer les doublons
        all_converation = list(set(all_converation))
        if user in all_converation :
                all_converation.remove(user)
              
        context = {
                'conversations' : all_converation,
                "messages" : messages,    
                "user_conversation" : user_conversation,
        }
        
        
        return render(request, f'gestion_messages/{user.type_utilisateur}/message.html', context)


def index(request):
        # Récupérer toutes les conversations et afficher les messages de la dernière conversation
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
        messages = Message.objects.filter(Q(expediteur=user) | Q(destinataire=user)).order_by('date_envoi')
        conversations = [ message.destinataire for message in messages if message.expediteur == user ] + [ message.expediteur for message in messages if message.destinataire == user ]
        #affacer les doublons
        conversations = list(set(conversations))
        if user in conversations :
                conversations.remove(user)
        
        
        context = {
                'conversations' : conversations,
        }
        
        
        return render(request, f'gestion_messages/{user.type_utilisateur}/message.html', context)

def recherche(request):
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
        
        if request.method == 'POST':
                mot_a_chercher = request.POST.get('recherche')
                # recuperer les messages contenant le mot recherche
                messages = Message.objects.filter(
                        Q(expediteur__nom__icontains=mot_a_chercher) |  # Recherche insensible à la casse dans le nom de l'expéditeur
                        Q(expediteur__prenom__icontains=mot_a_chercher) |  # Recherche insensible à la casse dans le prénom de l'expéditeur
                        Q(destinataire__nom__icontains=mot_a_chercher) |  # Recherche insensible à la casse dans le nom du destinataire
                        Q(destinataire__prenom__icontains=mot_a_chercher) |  # Recherche insensible à la casse dans le prénom du destinataire
                        Q(contenu__icontains=mot_a_chercher)  # Recherche insensible à la casse dans le contenu du message
                ).order_by('date_envoi')
                conversations = [ message.destinataire for message in messages if message.expediteur == user ] + [ message.expediteur for message in messages if message.destinataire == user ]
                #affacer les doublons
                #recuperer les utilisateur avec le mot a chercher
                resulat = Utilisateur.objects.filter(
                        Q(nom__icontains=mot_a_chercher) |  # Recherche insensible à la casse dans le nom de l'expéditeur
                        Q(prenom__icontains=mot_a_chercher) |
                        Q(telephone__icontains=mot_a_chercher)
                        # Recherche insensible à la casse dans le prénom de l'expéditeur
                )
                conversations = list(set(conversations)) + list(set(resulat))
                if user in conversations :
                        conversations.remove(user)
                context = {
                        'conversations' : conversations,
                }
                return render(request, f'gestion_messages/{user.type_utilisateur}/message.html', context)

        else :
                return redirect('gestion_messages:message')
                
def send(request, user_id):
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
        user_conversation = Utilisateur.objects.get(id=user_id)
        if request.method == 'POST':
                contenu = request.POST.get('contenu')
                message = Message(expediteur=user, destinataire=user_conversation, contenu=contenu)
                message.save()
        return redirect('gestion_messages:message' , user_id=user_conversation.id)