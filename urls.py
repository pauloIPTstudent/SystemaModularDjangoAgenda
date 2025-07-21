# agenda/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views


urlpatterns = [
    path('agendar/', views.agendar_compromisso_publico, name='agendar_publico'),
]

