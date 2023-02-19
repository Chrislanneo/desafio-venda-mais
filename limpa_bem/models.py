from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models


class Servico(models.Model):
    servico_id = models.AutoField(primary_key=True)
    descricao_servico = models.CharField(max_length=50, blank=False, null=False)
    preco_servico = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    disponibilidade = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    grupo = models.ForeignKey(Group,on_delete=models.PROTECT,default=1)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']

    def get_full_name(self):
        return f'{self.nome} {self.sobrenome}'

    def get_short_name(self):
        return self.nome

class Atendimento(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pendente'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )

    FORMA_PAGAMENTO = (
        ('C', 'Cartão'),
        ('E', 'Espécie'),
        ('B', 'Boleto'),
    )
    atendimento_id = models.AutoField(primary_key=True)
    tipo_servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    atendente = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='atendente')
    helper = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='helper')
    cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='cliente')
    desconto = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    forma_pagamento = models.CharField(max_length=1,choices=FORMA_PAGAMENTO)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)
    data_servico = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.desconto > 0.1:
            raise ValidationError("O desconto não pode ser maior que 10%.")

    def get_valor_total(self):
        preco_servico = self.tipo_servico.preco_servico
        valor_desconto = preco_servico * (self.desconto / 100)
        valor_total = preco_servico - valor_desconto
        return valor_total
