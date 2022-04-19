import csv
from io import StringIO
from django.contrib.auth.models import User

from agenda.serializers import PrestadorSerializer
from tamarcado.celery import app


@app.task
def gera_relatorio_prestadores():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "prestador",
        "nome_cliente",
        "email_cliente",
        "data_horario"
    ])
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    for prestador in serializer.data:
        agendamentos = prestador["agendamentos"]
        for agendamento in agendamentos:
            writer.writerow([
                agendamento["prestador"],
                agendamento["nome_cliente"],
                agendamento["email_cliente"],
                agendamento["data_horario"]
            ])