import email
from pickle import GET
import re
from wsgiref import validate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializar

# Create your views here.

@api_view(http_method_names=["GET","PUT"])
def agendamento_detail(request,id):
    if request.method == "GET":
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializar(obj)
        return JsonResponse(serializer.data)
    if request.method == "PUT":
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializar(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            obj.data_horario = validated_data.get("data_horario", obj.data_horario)
            obj.nome_cliente = validated_data.get("nome_cliente", obj.nome_cliente)
            obj.email_cliente = validated_data.get("email_cliente", obj.email_cliente)
            obj.telefone_cliente = validated_data.get("telefone_cliente", obj.telefone_cliente)
            obj.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

@api_view(http_method_names=["GET","POST"])
def agendamento_list(request):
    if request.method == "GET":
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializar(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = request.data
        serializer = AgendamentoSerializar(data=data)
        if serializer.is_valid():
            validated_date = serializer.validated_data
            Agendamento.objects.create(
                data_horario = validated_date["data_horario"],
                nome_cliente=validated_date["nome_cliente"],
                email_cliente=validated_date["email_cliente"],
                telefone_cliente=validated_date["telefone_cliente"]
            )
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors, status=400)