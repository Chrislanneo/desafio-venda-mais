from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .models import Servico, Usuario, Atendimento
from .serializers import ServicoSerializer, AtendimentoSerializer, UsuarioSerializer

@api_view(['POST'])
def cadastrar_usuario(request):
    usuario = Usuario.objects.filter(id=request.user.id).first()
    if str(usuario.grupo) == ('gerente'):
        serializer = AtendimentoSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                grupo_id = request.data.get('grupo', None)
                grupo = Group.objects.filter(id=grupo_id).first()
                if not grupo:
                    return Response({'error': 'Grupo não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    error_message = {'Usuário não é autorizado para essa ação.'}
    return Response(error_message, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cadastrar_servico(request):
    usuario = Usuario.objects.filter(id=request.user.id).first()
    if str(usuario.grupo) == ('gerente'):
        serializer = ServicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    error_message = {'Usuário não é autorizado para essa ação.'}
    return Response(error_message, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cadastrar_atendimento(request):
    usuario = Usuario.objects.filter(id=request.user.id).first()
    if str (usuario.grupo) == ('gerente') or str (usuario.grupo) == ('atendente'):
        serializer = AtendimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    error_message = {'Usuário não é autorizado para essa ação.'}
    return Response(error_message, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_atendimento(request):
    usuario = Usuario.objects.filter(id=request.user.id).first()
    if str(usuario.grupo) == ('cliente'):
        serializer = AtendimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    error_message = {'Usuário não é autorizado para essa ação.'}
    return Response(error_message, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_servicos(request):
    servico = Servico.objects.all()
    serializer = ServicoSerializer(servico, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def listar_atendimentos(request):
    atendimento = Atendimento.objects.all()
    serializer = AtendimentoSerializer(atendimento, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def relatorio_valor_total(request):
    data = request.query_params.get('data')
    if not data:
        return JsonResponse({'error': 'A data é obrigatória.'}, status=400)
    try:
        data = parse_date(data)
    except ValueError:
        return JsonResponse({'error': 'Data inválida.'}, status=400)

    atendimentos = Atendimento.objects.filter(data_servico=data)
    valor_total = atendimentos.aggregate(Sum('valor'))['valor__sum'] or 0
    return JsonResponse({'valor_total': valor_total})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consultar_atendimento(request, atendimento_id):
    try:
        atendimento = Atendimento.objects.get(atendimento_id=atendimento_id)
        serializer = AtendimentoSerializer(atendimento)
        return Response(serializer.data)
    except Atendimento.DoesNotExist:
        return Response({'message': 'Atendimento não encontrado'}, status=404)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_atendimento(request, atendimento_id):
    try:
        atendimento = Atendimento.objects.get(atendimento_id=atendimento_id)
    except Atendimento.DoesNotExist:
        return Response({'message': 'Atendimento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AtendimentoSerializer(atendimento, data=request.data, partial=True)
    usuario = Usuario.objects.filter(id=request.user.id).first()
    if str (usuario.grupo) == ('gerente'):
        if serializer.is_valid():
            serializer.update_gerente(atendimento,request.data)
            return Response(serializer.data)
    if str (usuario.grupo) == ('gerente') or str (usuario.grupo) == ('atendente'):
        if serializer.is_valid():
            serializer.update_atendente()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    error_message = {'Usuário não é autorizado para essa ação.'}
    return Response(error_message, status=401)

def index(request):
    return render(request, 'index.html')
