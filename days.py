import calendar


def first_lasted_day(ano, mes):
    # Use o módulo calendar para obter o primeiro e o último dia do mês
    primeiro_dia = f'01/{mes}/{ano}'
    ultimo_dia = f'{calendar.monthrange(ano, mes)[1]}/{mes}/{ano}'  # Último dia do mês

    return primeiro_dia, ultimo_dia


if __name__ == '__main__':

    # Exemplo de uso:
    ano = 2023
    mes = 2
    primeiro_dia, ultimo_dia = first_lasted_day(ano, mes)

    print(f'Primeiro dia: {primeiro_dia}')
    print(f'Último dia: {ultimo_dia}')
