from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Agenda
from django.contrib.admin.sites import site
from .models import AgendaCompromisso


@admin.register(AgendaCompromisso)
class AgendaCompromissoAdmin(admin.ModelAdmin):
    list_display = ('titulo',  'agenda', 'data_inicio', 'data_fim', 'status', 'local', 'cliente')
    list_filter = ('agenda','data_inicio', 'data_fim', 'status', 'local', 'cliente')
    search_fields = ('titulo', 'descricao')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filtra compromissos pela agenda do usuário logado
        return qs.filter(agenda__usuario=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        return obj.agenda.usuario == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        return obj.agenda.usuario == request.user
# VIEW customizada
def minha_pagina_customizada(request):
    context = {'title': ' Angenda',
               'app_list': admin.site.get_app_list(request),
        'available_apps': admin.site.get_app_list(request), }
    return render(request, 'admin/minha_pagina_customizada.html', context)

# ADMIN do modelo Agenda
@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    change_list_template = "admin/agenda_change_list.html"  # opcional

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('minha-pagina/', self.admin_site.admin_view(minha_pagina_customizada), name='minha-pagina'),
        ]
        return custom_urls + urls
