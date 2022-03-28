from re import M
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset