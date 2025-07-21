# agenda/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
from .views import (
    AgendaViewSet, AgendaCompromissoViewSet,
    AgendaTipoViewSet, AgendaParticipanteViewSet
)

router = DefaultRouter()
router.register(r'agendas', AgendaViewSet, basename='agenda')
router.register(r'compromissos', AgendaCompromissoViewSet, basename='compromisso')
router.register(r'tipos', AgendaTipoViewSet, basename='tipo')
router.register(r'participantes', AgendaParticipanteViewSet, basename='participante')


urlpatterns = router.urls