from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Agenda
from django.contrib.admin.sites import site

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
