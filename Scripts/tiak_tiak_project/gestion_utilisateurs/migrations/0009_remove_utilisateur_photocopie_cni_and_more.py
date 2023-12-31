# Generated by Django 4.2.5 on 2023-10-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateurs', '0008_livreur_on_mission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='photocopie_cni',
        ),
        migrations.AddField(
            model_name='livreur',
            name='photocopie_cni',
            field=models.ImageField(blank=True, null=True, upload_to='photocopies_cni/'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='sexe',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
