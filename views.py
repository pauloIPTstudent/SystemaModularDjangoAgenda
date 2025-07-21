from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Agenda, AgendaCompromisso, AgendaTipo, AgendaParticipante
from .serializers import (
    AgendaSerializer, AgendaCompromissoSerializer,
    AgendaTipoSerializer, AgendaParticipanteSerializer
)
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json
from django.utils.timezone import now


class AgendaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgendaSerializer

    def get_queryset(self):
        # usuário só vê sua própria agenda
        return Agenda.objects.filter(usuario=self.request.user)

    def get_object(self):
        # retorna a agenda do usuário logado
        return self.get_queryset().first()


class AgendaCompromissoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgendaCompromissoSerializer

    def get_queryset(self):
        # compromissos do usuário logado
        return AgendaCompromisso.objects.filter(agenda__usuario=self.request.user)

    def perform_create(self, serializer):
        # força o compromisso a pertencer à agenda do usuário logado
        agenda = Agenda.objects.get(usuario=self.request.user)
        serializer.save(agenda=agenda)


class AgendaTipoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = AgendaTipo.objects.all()
    serializer_class = AgendaTipoSerializer


class AgendaParticipanteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgendaParticipanteSerializer

    def get_queryset(self):
        # só participantes de compromissos do usuário
        return AgendaParticipante.objects.filter(compromisso__agenda__usuario=self.request.user)
        
  
@staff_member_required
def admin_calendar_view(request):
    return render(request, "agenda/admin_calendar.html")

@staff_member_required
def calendar_events_api(request):
    user = request.user
    compromissos = AgendaCompromisso.objects.filter(agenda__usuario=user, status='agendado')
    eventos = [{
        "id": c.id,
        "title": c.titulo,
        "start": c.data_inicio.isoformat(),
        "end": c.data_fim.isoformat(),
        "color": c.tipo.cor if c.tipo else "#3788d8",
    } for c in compromissos]
    return JsonResponse(eventos, safe=False)

@staff_member_required
@csrf_exempt
def calendar_create_event_api(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        titulo = data.get('title')
        start = parse_datetime(data.get('start'))
        end = parse_datetime(data.get('end'))
        if not titulo or not start or not end:
            return JsonResponse({"error": "Dados inválidos"}, status=400)
        agenda = user.agenda
        compromisso = AgendaCompromisso.objects.create(
            agenda=agenda,
            titulo=titulo,
            data_inicio=start,
            data_fim=end,
            status='agendado'
        )
        return JsonResponse({
            "id": compromisso.id,
            "title": compromisso.titulo,
            "start": compromisso.data_inicio.isoformat(),
            "end": compromisso.data_fim.isoformat()
        })
    return JsonResponse({"error": "Método não permitido"}, status=405)

def agendar_compromisso_publico(request):
    agendas = Agenda.objects.all()
    tipos = AgendaTipo.objects.all()
    if request.method == "POST":
        agenda_id = request.POST.get("agenda_id")
        tipo_id = request.POST.get("tipo_id")


        
        return redirect("agenda/agenda_sucesso")
    return render(request, "agenda/agendar_publico.html",{"agendas":agendas,"tipos":tipos} )