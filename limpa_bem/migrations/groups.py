from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    # Cria o grupo "Administradores"
    admin_group = Group(name='Administradores')
    admin_group.save()

    # Cria o grupo "Atendentes"
    atendente_group = Group(name='Atendentes')
    atendente_group.save()

    # Cria o grupo "Clientes"
    cliente_group = Group(name='Clientes')
    cliente_group.save()

    # Cria o grupo "Helper"
    helper_group = Group(name='Helper')
    helper_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('limpa_bem', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
