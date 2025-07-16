from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Agenda

User = get_user_model()

@receiver(post_save, sender=User)
def criar_agenda_usuario(sender, instance, created, **kwargs):
    if created:
        Agenda.objects.create(usuario=instance)
