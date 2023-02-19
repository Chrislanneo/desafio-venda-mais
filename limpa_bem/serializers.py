from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Servico, Atendimento, Usuario
from django.contrib.auth.models import Group
from datetime import datetime, timedelta



class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['descricao_servico', 'preco_servico', 'disponibilidade']

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    grupo = serializers.IntegerField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'nome', 'sobrenome', 'password', 'grupo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        grupo_id = validated_data.pop('grupo')
        usuario = Usuario.objects.create(**validated_data)
        grupo = Group.objects.get(id=grupo_id)
        usuario.grupo = grupo
        usuario.save()
        return usuario

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'

    def update_gerente(self, instance, validated_data):
        novo_desconto = validated_data.get('desconto')
        if novo_desconto is not None and novo_desconto > 10:
            raise serializers.ValidationError("O desconto não pode ser maior que 10%.")
        instance.desconto = novo_desconto if novo_desconto is not None else instance.desconto
        instance.save()
        return instance

    def update_atendente(self, instance, validated_data):
        instance.data_servico = validated_data.get('data_servico', instance.data_servico)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

