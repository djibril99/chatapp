from .models import Utilisateur


def utilisateur_connecte(request):
    user_id = request.session.get('user_id')
    if user_id:
        utilisateur = Utilisateur.objects.get(id=user_id)
        return  {'user': utilisateur}
    else:
        return {}