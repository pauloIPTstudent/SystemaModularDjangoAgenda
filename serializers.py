from rest_framework import serializers
from .models import Agenda, AgendaCompromisso, AgendaParticipante, AgendaTipo
from django.contrib.auth import get_user_model

User = get_user_model()

class AgendaTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaTipo
        fields = ['id', 'nome', 'cor']


class AgendaParticipanteSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', write_only=True
    )

    class Meta:
        model = AgendaParticipante
        fields = ['id', 'compromisso', 'usuario', 'usuario_id', 'presenca_confirmada']


class AgendaCompromissoSerializer(serializers.ModelSerializer):
    tipo = AgendaTipoSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(
        queryset=AgendaTipo.objects.all(), source='tipo', write_only=True
    )
    participantes = AgendaParticipanteSerializer(many=True, read_only=True)

    class Meta:
        model = AgendaCompromisso
        fields = [
            'id', 'agenda', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'tipo', 'tipo_id',
            'status', 'local', 'cliente', 'observacoes', 'data_criacao', 'participantes'
        ]
        read_only_fields = ['data_criacao']


class AgendaSerializer(serializers.ModelSerializer):
    compromissos = AgendaCompromissoSerializer(many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ['id', 'usuario', 'nome', 'descricao', 'compromissos']
        read_only_fields = ['usuario']
        #extra_kwargs = {
        #    'nome': {'required': False, 'default': 'Agenda Pessoal'},
        #    'descricao': {'required': False, 'default': ''}
        #}