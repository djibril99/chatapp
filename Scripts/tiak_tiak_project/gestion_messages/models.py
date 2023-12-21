from django.db import models
from gestion_utilisateurs.models import Utilisateur


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_as_dest', null=True)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_as_exp', null=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.conversation.expediteur.nom} à {self.conversation.destinataire.nom} le {self.date_envoi}"
