from datetime import datetime, timezone
import json
from rest_framework.test import APITestCase

from agenda.models import Agendamento

# Create your tests here.

class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=datetime(2022,3,28),
            nome_cliente="Alice",
            email_cliente="alice@codar.me",
            telefone_cliente="12345678",
        )

        agendamento_serializado = {
            "id":1,
            "data_horario":"2022-03-28T00:00:00Z",
            "nome_cliente":"Alice",
            "email_cliente":"alice@codar.me",
            "telefone_cliente":"12345678"
        }
        
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)

class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        # agendamento_request_data = {
        #     "data_horario":"2022-03-28 00:00:00",
        #     "nome_cliente":"Alice",
        #     "email_cliente":"alice@codar.me",
        #     "telefone_cliente":"12345678",
        # }

        Agendamento.objects.create(
            data_horario=datetime(2022,3,28),
            nome_cliente="Alice",
            email_cliente="alice@codar.me",
            telefone_cliente="12345678",
        )

        # response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

        agendamento_criado = Agendamento.objects.get()

        self.assertEqual(agendamento_criado.data_horario, datetime(2022, 3, 28, tzinfo=timezone.utc))

 
