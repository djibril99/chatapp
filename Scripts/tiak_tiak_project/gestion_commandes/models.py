from django.db import models
from django.utils import timezone
from gestion_utilisateurs.models import Client, Livreur
class Marchandise(models.Model):
        client = models.ForeignKey(Client, on_delete=models.CASCADE)
        #ajouter une photo  de la marchandise
        photo =models.ImageField(upload_to='photo_marchandise/', null=True, blank=True)
        description = models.CharField(max_length=500, null=True)
        poids = models.FloatField(null=False , default=0)        
        def __str__(self):
                return f'Marchandise de {self.client.user.prenom} {self.client.user.nom}'
        
class Livraison(models.Model):
        id = models.AutoField(primary_key=True)
        livreur = models.ForeignKey(Livreur, on_delete= models.SET_NULL, null=True)
        marchandise = models.ForeignKey(Marchandise, on_delete=models.CASCADE)
        #point gps de depart 
        longitude_depart = models.FloatField( null=False)
        latitude_depart = models.FloatField( null=False)
        #point gps d'arrivée
        longitude_arrivee = models.FloatField(null = False)
        latitude_arrivee = models.FloatField( null=False)
        #date et heure de livraison
        date_livraison = models.DateTimeField(default=timezone.now)
        #etat de la livraison boolean
        etat_livraison = models.BooleanField(default=False)
        #mode de livraison (aerien, terrestre)
        #i y a deux valeurs possibles : aerien et terrestre
        MODE_LIVRAISON = (
                ('aerien', 'aerien'),
                ('terrestre', 'terrestre'),
        )
        mode_livraison = models.CharField(max_length=10, choices=MODE_LIVRAISON, default=MODE_LIVRAISON[0][1])
        #code de validation de la livraison , par le client (une chaine de 150 caractere generée aleatoirement)
        code_validation = models.CharField(max_length=150 , null=True)
        def __str__(self):
                return f"Livraison du {self.date_livraison} de {self.marchandise.client.user.prenom} {self.marchandise.client.user.nom}"