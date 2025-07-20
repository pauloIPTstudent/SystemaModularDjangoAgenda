import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Agenda(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agenda')
    nome = models.CharField(max_length=100, default="Agenda Pessoal")
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Agenda de {self.usuario.username}"


class AgendaTipo(models.Model):
    nome = models.CharField(max_length=100)
    cor = models.CharField(max_length=7, default="#3788d8")

    def __str__(self):
        return self.nome


class AgendaCompromisso(models.Model):
        
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='compromissos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.ForeignKey(AgendaTipo, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    local = models.CharField(max_length=255, blank=True)
    cliente = models.UUIDField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} ({self.data_inicio.date()})'
    
    class Meta:
        verbose_name = "Compromisso"
        verbose_name_plural = "Compromissos"

class AgendaParticipante(models.Model):
    compromisso = models.ForeignKey(AgendaCompromisso, on_delete=models.CASCADE, related_name='participantes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    presenca_confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario} em {self.compromisso}'
