from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ["id", "data_horario", "nome_cliente", "email_cliente", "telefone_cliente", "prestador"]

    prestador = serializers.CharField()
    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username não existe!")
        return prestador_obj


    def validate_data_horario(self, value):
        if(value < timezone.now()):
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("Este horário não esta dispovível")
        return value


    def validate_telefone_cliente(self, value):
        if(len(value) < 8):
            raise serializers.ValidationError("O numero é muito curto!")
        for char in value:
            if (char == "+"):
                if (value[0] != char):
                    raise serializers.ValidationError("Caracter inválido!")

            elif ( char != "(" and char != ")" and char != "-"):
                if not ("0" <= char <= "9"):
                    raise serializers.ValidationError("Caracter inválido!")



        return value

#    def validate(self, attrs):
#        telefone_cliente = attrs.get("telefone_cliente", "")
#        email_cliente = attrs.get("email_cliente")

#        if(email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswithc("+55")):
#            raise serializers.ValidationError("Email brasileiro deve estar associado a um númedo no Brasil.")
#        return attrs


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos']
    
    agendamentos = AgendamentoSerializer(many=True, read_only=True)

