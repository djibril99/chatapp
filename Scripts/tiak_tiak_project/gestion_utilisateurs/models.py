from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    #attribut de l utilisateur
    nom = models.CharField(null=True,max_length=255)
    prenom = models.CharField(null=True,max_length=255)
    sexe =  models.CharField(null=True,max_length=1)
    
    email = models.EmailField(null=True,max_length=255)
    
    date_naissance = models.DateField(null=True)
    adresse = models.CharField(null=True,max_length=255)
    telephone = models.IntegerField(null=True)
    
    photo_identite = models.ImageField(upload_to='photos_identite/', null=True, blank=True)
    
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #ajouter le type d utilisateur pour l indentifier lors de la connexion
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('livreur', 'Livreur'),
        ('admin', 'Admin')
    )

    # Autres champs d'utilisateur
    type_utilisateur = models.CharField(max_length=10, choices=ROLE_CHOICES , default=ROLE_CHOICES[0][0])
    online = models.BooleanField(default=False)


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    # Vous pouvez ajouter des attributs spécifiques au client ici si nécessaire
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE , default=None )
    def __str__(self):
        return self.user.prenom 

class Livreur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, default=None )
    photocopie_cni = models.ImageField(upload_to='photocopies_cni/', null=True, blank=True)
    
    #attibut de localisation
    latitude = models.FloatField(null=True, blank=True) #
    longitude = models.FloatField(null=True, blank=True)
    #verifier si le livreur est actif (par l admin)
    actif = models.BooleanField(default=False)
    on_mission = models.BooleanField(default=False)
    # Ajoutez d'autres attributs spécifiques au livreur ici si nécessaire
    def __str__(self):
        return self.user.prenom  # Utilisez un attribut approprié pour l'identification du livreur

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, default=None )
    # Vous pouvez ajouter des attributs spécifiques à l'administrateur ici si nécessaire
    def __str__(self):
        return self.user.prenom   # Utilisez un attribut approprié pour l'identification de l'administrateur
