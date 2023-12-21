# Generated by Django 4.2.5 on 2023-09-16 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateurs', '0001_initial'),
        ('gestion_commandes', '0002_remove_marchandise_poids'),
        ('gestion_notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='recipients',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='sender',
        ),
        migrations.AddField(
            model_name='notification',
            name='livreur_choisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_utilisateurs.livreur'),
        ),
        migrations.AddField(
            model_name='notification',
            name='livreurs_recus',
            field=models.ManyToManyField(blank=True, related_name='notifications_recues_liste', to='gestion_utilisateurs.livreur'),
        ),
        migrations.AddField(
            model_name='notification',
            name='marchandise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_commandes.marchandise'),
        ),
    ]
