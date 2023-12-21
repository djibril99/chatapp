from django.urls import path
from . import views
app_name = 'gestion_messages'

urlpatterns = [
        path('', views.index, name='message'),
        path('message/<int:user_id>/', views.lire_message, name='message'),
        path('recherche/', views.recherche, name='recherche'),
        path('send/<int:user_id>/', views.send, name='send')
]