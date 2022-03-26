from pickle import GET
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializar

# Create your views here.

@api_view(http_method_names=["GET"])
def agendamento_detail(request,id):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializar(obj)
    return JsonResponse(serializer.data)

@api_view(http_method_names=["GET"])
def agendamento_list(request):
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializar(qs, many=True)
    return JsonResponse(serializer.data, safe=False)