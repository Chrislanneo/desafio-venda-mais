
from django.contrib import admin
from django.urls import path

from limpa_bem.views import cadastrar_servico, cadastrar_atendimento, cadastrar_usuario, listar_atendimentos, \
    atualizar_atendimento, consultar_atendimento, listar_servicos, relatorio_valor_total, agendar_atendimento, index

urlpatterns = [
    path('/', admin.site.urls),
    path('servicos/', cadastrar_servico, name='cadastrar_servico'),
    path('atendimento/', cadastrar_atendimento, name='cadastrar_atendimento'),
    path('atendimento/agendar', agendar_atendimento, name='cadastrar_atendimento'),
    path('usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('atendimento/relatorio/lista-atendimentos/', listar_atendimentos, name='listar_atendimentos'),
    path('atendimento/relatorio/valor-total/', relatorio_valor_total, name='relatorio-valor-total'),
    path('servico/listagem/', listar_servicos, name='listar_servico'),
    path('atendimento/<int:atendimento_id>/consultar/',consultar_atendimento, name='consultar_atendimento'),
    path('atendimento/<int:atendimento_id>/atualizar/',atualizar_atendimento, name='atualizar_atendimento'),
    path('', index)

]
