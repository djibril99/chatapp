# Generated by Django 4.2.5 on 2023-10-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateurs', '0009_remove_utilisateur_photocopie_cni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='type_utilisateur',
            field=models.CharField(choices=[('client', 'Client'), ('livreur', 'Livreur'), ('admin', 'Admin')], default='client', max_length=10),
        ),
    ]
