from django.contrib import admin
from .models import Utilisateur, Client , Livreur , Admin

#ajout de la classe Utilisateur dans l'interface d'administration
admin.site.register(Utilisateur)
admin.site.register(Client)
admin.site.register(Livreur)
admin.site.register(Admin)