from django.db import migrations

def adiciona_dados_iniciais(apps, schema_editor):
    # Importa o modelo que você deseja usar
    Servico = apps.get_model('limpa_bem', 'Servico')

    # Cria um objeto e salva no banco de dados
    servico_1 = Servico(descricao_servico='Limpeza Profunda', preco_servico=250.00, disponibilidade= True)
    servico_1.save()

    servico_2 = Servico(descricao_servico='Limpeza Simples', preco_servico=100.00, disponibilidade= True)
    servico_2.save()

class Migration(migrations.Migration):
    dependencies = [
        ('limpa_bem', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(adiciona_dados_iniciais),
    ]
