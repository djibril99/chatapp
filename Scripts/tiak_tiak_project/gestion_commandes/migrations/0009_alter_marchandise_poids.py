# Generated by Django 4.2.5 on 2023-12-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_commandes', '0008_livraison_mode_livraison_marchandise_poids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marchandise',
            name='poids',
            field=models.FloatField(default=0),
        ),
    ]
