
from django import forms
from .models import Utilisateur
#importer DateInput
from django import forms
from .models import Utilisateur, Client, Livreur

class InscriptionForm(forms.ModelForm):
    # Ajoutez un champ pour spécifier le type d'utilisateur (client ou livreur)
    utilisateur_type = forms.ChoiceField(
        choices=[
            ('client', 'Client'),
            ('livreur', 'Livreur'),
        ],
        widget=forms.RadioSelect
    )
    password_confirm = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label='Confirmer le mot de passe'
    )
    sexe =  forms.CharField( widget=forms.RadioSelect, required=False)
    photocopie_cni = forms.ImageField(required=False)
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email','adresse', 'date_naissance', 'telephone', 'password', 'password_confirm','sexe','photocopie_cni']
    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur_type = self.cleaned_data['utilisateur_type']
        
        # Ajoutez le type d'utilisateur à l'instance utilisateur
        utilisateur.type_utilisateur = utilisateur_type

        if utilisateur_type == 'client':
            client = Client(user=utilisateur)
            if commit:
                utilisateur.save()
                client.save()
        elif utilisateur_type == 'livreur':
            livreur = Livreur(user=utilisateur, photocopie_cni=self.cleaned_data['photocopie_cni'])
            if commit:
                utilisateur.save()
                livreur.save()

        return utilisateur
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')

        return cleaned_data
    
    
class  ConnectionForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['telephone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class UpdateProfil(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['prenom', 'nom', 'telephone', 'email', 'date_naissance', 'adresse', 'photo_identite', 'password', 'new_password', 'confirm_password',"sexe"]
    
    photo_identite = forms.ImageField(required=False)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput() , required=False)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=False)
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    sexe =  forms.CharField( widget=forms.RadioSelect, required=False)

    def clean(self):
        cleaned_data = super().clean()
        # Vous pouvez ajouter des validations personnalisées ici si nécessaire

    def save(self, user=None):
       
        if user:
            if user.password == self.cleaned_data.get("password"):
                if self.cleaned_data.get("new_password") == self.cleaned_data.get("confirm_password") and self.cleaned_data.get("new_password") != "":
                    user.password = self.cleaned_data.get("new_password")
                if self.cleaned_data.get("prenom") != "":
                    user.prenom = self.cleaned_data.get("prenom")
                if self.cleaned_data.get("nom") != "":
                    user.nom = self.cleaned_data.get("nom")
                if self.cleaned_data.get("email") != "":
                    user.email = self.cleaned_data.get("email")
                if self.cleaned_data.get("telephone") != "":
                    user.telephone = self.cleaned_data.get("telephone")
                if self.cleaned_data.get("date_naissance") != "" and self.cleaned_data.get("date_naissance") != None:
                    user.date_naissance = self.cleaned_data.get("date_naissance")
                if self.cleaned_data.get("adresse") != "":
                    user.adresse = self.cleaned_data.get("adresse")
                if self.cleaned_data.get("photo_identite") != "":
                    user.photo_identite = self.cleaned_data.get("photo_identite")
                if self.cleaned_data.get("sexe") != "":
                    user.sexe = self.cleaned_data.get("sexe")
                user.save()
        return user
