# Generated by Django 4.2.5 on 2023-09-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_commandes', '0005_alter_marchandise_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]