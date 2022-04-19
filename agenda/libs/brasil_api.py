from datetime import date
import requests

import logging

from django.conf import settings

def is_feriado(data: date) -> bool:
    logging.info(f"Fazendo uma requisição para BrasilAPI para a data: {data.isoformat()}")
    if settings.TESTING == True:
        logging.info("Requisição não está sendo feita pois TESTING = True")
        if data.day == 25 and data.month == 12:
            return True
        return False    



    ano = data.year
    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if not r.status_code == 200:
        logging.error("Algum erro ocorreu em Brasil API")
        return False
    feriados = r.json()
    for feriado in feriados:
        data_horario_as_str = feriado["date"]
        data_feriado = date.fromisoformat(data_horario_as_str)
        if data == data_feriado:
            return True

    return False