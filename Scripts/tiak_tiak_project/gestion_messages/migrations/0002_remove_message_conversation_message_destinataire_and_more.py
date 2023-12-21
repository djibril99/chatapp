# Generated by Django 4.2.5 on 2023-09-30 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateurs', '0006_alter_admin_id_alter_client_id_alter_livreur_id_and_more'),
        ('gestion_messages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.AddField(
            model_name='message',
            name='destinataire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_dest', to='gestion_utilisateurs.utilisateur'),
        ),
        migrations.AddField(
            model_name='message',
            name='expediteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_exp', to='gestion_utilisateurs.utilisateur'),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
    ]