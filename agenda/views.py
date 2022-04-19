from datetime import datetime
from unittest import result
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.tasks import gera_relatorio_prestadores
from agenda.utils import get_horarios_disponiveis

import csv
from datetime import date

# Create your views here.
class IsOwnerOrCreateOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username",None)
        if request.user.username == username:
            return True    
        return False

class isPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[isPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def perform_destroy(self, instance):
        instance.cancelado = False
        instance.save()

    

class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        queryset = Agendamento.objects.filter(cancelado = False)
        return queryset

# class PrestadorList(generics.ListAPIView):
#     serializer_class = PrestadorSerializer
#     queryset = User.objects.all()

@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAdminUser])
def relatorio_prestadores(request):

    if request.query_params.get("formato") == "csv":
        data_hoje = date.today()
        # response = HttpResponse(
        #     content_type = 'text/csv',
        #     headers={'Content-Disposition':f'attachment; filename="relatorio_{data_hoje}.csv"'}
        # )
        result = gera_relatorio_prestadores.delay()
        return Response({"task_id": result.task_id})
    else:
        prestadores = User.objects.all()
        serializer = PrestadorSerializer(prestadores, many=True)
        return Response(serializer.data)

@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return Response(horarios_disponiveis)

@api_view(http_method_names=["GET"])
def healthcheck(request):
    return Response({"status":"Ok"}, status=200)