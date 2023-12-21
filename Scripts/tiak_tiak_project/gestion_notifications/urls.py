from django.urls import path
from . import views

app_name = 'gestion_notifications'

urlpatterns = [
        path('', views.index, name='index'),
        
        path('stream_notifications/', views.liste_notification_livreur_streaming, name='stream_notifications'),
        path('postuler/<int:notification_id>/', views.postuler_livraison, name='postuler'),
        path('annuler/<int:notification_id>/', views.annuler_postule, name='annuler'),
        path('accepter/<int:notification_id>/', views.accepter_postule , name= 'choisir_livreur'),
        #administrateur
        path('liste_notifications/<int:id_utilisateur>', views.liste_notification_admin, name='liste_notifications'),
        path('supprimer/<int:id_notification>/<int:id_utilisateur>',views.supprimer , name= 'supprimer'),
        path('detail/<int:id_notification>/<int:id_utilisateur>',views.detail_notification , name= 'detail'),
]
