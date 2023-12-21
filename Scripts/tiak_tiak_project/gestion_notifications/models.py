from django.db import models
from gestion_utilisateurs.models import Livreur
from gestion_commandes.models import Marchandise
from gestion_commandes.models import Livraison


class Postulation(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    livraison = models.ForeignKey(Livraison, on_delete=models.CASCADE, null=True, blank=True)
    livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE, null=True, blank=True)
    prixPropose = models.FloatField(null=True, blank=True)
    
    
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    livraison = models.ForeignKey(Livraison, on_delete=models.CASCADE, null=True, blank=True)
    # Nouveaux champs pour suivre les livreurs
    livreurs_postule = models.ManyToManyField(Livreur, related_name='livreurs_postule_liste', blank=True)
    postulation = models.ManyToManyField(Postulation, related_name='Postulation_liste', blank=True)
    
    def __str__(self):
        return f"Notification ({self.id})"
