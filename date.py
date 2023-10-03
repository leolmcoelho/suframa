import os
import calendar
from datetime import datetime

def first_lasted_day(ano, mes):
    # Use o módulo calendar para obter o primeiro e o último dia do mês
    primeiro_dia = f'01/{mes}/{ano}'
    ultimo_dia = f'{calendar.monthrange(ano, mes)[1]}/{mes}/{ano}'  # Último dia do mês

    return primeiro_dia, ultimo_dia

def day_now():
    data_atual = datetime.now()
    dia = data_atual.strftime('%d')
    mes = data_atual.strftime('%m')
    ano = data_atual.strftime('%Y')
    return ano, mes, dia

def make_path():
    ano, mes, _ = day_now()
    ano_mes = f'{ano}\\{mes}-{ano}'
    path = os.path.join('G:\\Meu Drive\\ENCONTADORES\\[1- CENTRAL DE OBRIGACOES E ARQUIVOS]',
                        f'1 - IMPOSTOS - TRIBUTOS - TAXAS\\1 - SUFRAMA\\{ano}\\{ano_mes}')
    return path


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        



if __name__ == '__main__':

    # Exemplo de uso:
    ano = 2023
    mes = 2
    primeiro_dia, ultimo_dia = first_lasted_day(ano, mes)

    print(f'Primeiro dia: {primeiro_dia}')
    print(f'Último dia: {ultimo_dia}')
