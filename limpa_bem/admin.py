from django.contrib import admin
from .models import Servico, Usuario


class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao_servico', 'preco_servico', 'disponibilidade')

admin.site.register(Servico, ServicoAdmin)
admin.site.register(Usuario)