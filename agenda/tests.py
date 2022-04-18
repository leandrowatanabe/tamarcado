from datetime import datetime, timezone
from email.mime import application
import json
from typing import Tuple
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from agenda.models import Agendamento

from unittest import mock

# Create your tests here.

class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        user = User.objects.create(email="teste@codar.me", username="teste", password="123")
        self.client.force_authenticate(user)
        response = self.client.get("/api/agendamentos/?username=teste")
        data = json.loads(response.content)
        assert data == []

    def test_listagem_de_agendamentos_criados(self):
        user = User.objects.create(email="teste@codar.me", username="teste", password="123")
        self.client.force_authenticate(user)

        Agendamento.objects.create(
            data_horario=datetime(2022,3,28,tzinfo=timezone.utc),
            nome_cliente="Alice",
            email_cliente="alice@codar.me",
            telefone_cliente="12345678",
            prestador=User.objects.get(id=1),
            cancelado = False
        )

        agendamento_serializado = {
            "id":1,
            "data_horario":"2022-03-28T00:00:00Z",
            "nome_cliente":"Alice",
            "email_cliente":"alice@codar.me",
            "telefone_cliente":"12345678",
            "prestador":"teste"
        }
        
        response = self.client.get("/api/agendamentos/?username=teste")
        data = json.loads(response.content)
        assert data[0] == agendamento_serializado

    def test_listagem_acessado_por_outro_user(self):
        user1 = User.objects.create(email="teste@codar.me", username="teste", password="123")
        self.client.force_authenticate(user1)

        Agendamento.objects.create(
            data_horario=datetime(2022,3,28,tzinfo=timezone.utc),
            nome_cliente="Alice",
            email_cliente="alice@codar.me",
            telefone_cliente="12345678",
            prestador=User.objects.get(id=1),
            cancelado = False
        )
        
        response = self.client.get("/api/agendamentos/?username=random")
        assert response.status_code == 403

class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):

        user = User.objects.create(email="teste@codar.me", username="teste", password="123")
        self.client.force_authenticate(user)

        Agendamento.objects.create(
            data_horario=datetime(2022,3,28),
            nome_cliente="Alice",
            email_cliente="alice@codar.me",
            telefone_cliente="12345678",
            prestador=User.objects.get(id=1),
            cancelado = False
        )

        # response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

        agendamento_criado = Agendamento.objects.get()

        assert (agendamento_criado.data_horario == datetime(2022, 3, 28, tzinfo=timezone.utc))

    def test_cria_agendamento_status(self):

        user = User.objects.create(email="teste@codar.me", username="teste", password="123")
        self.client.force_authenticate(user)


        agendamento_criado = { 
            "data_horario":"2022-04-25T10:00:00Z",
            "nome_cliente":"Alice",
            "email_cliente":"alice@codar.me",
            "telefone_cliente":"12345678",
            "prestador":"teste",
        }

        response = self.client.post("/api/agendamentos/", agendamento_criado)
   
        assert response.status_code == 201

class TestGetHorarios(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        response = self.client.get("/api/horarios/?data=2022-12-25")
        assert response.data == []

    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_retorna_lista(self, _):
        response = self.client.get("/api/horarios/?data=2022-04-18")
        assert response.data != []
        assert response.data[0] == datetime(2022, 4, 18, 9, tzinfo=timezone.utc)
        assert response.data[-1] == datetime(2022, 4, 18, 17, 30, tzinfo=timezone.utc)


