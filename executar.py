import os
from suframa import Suframa
import pandas as pd
import time
from days import first_lasted_day

import calendar

from datetime import datetime


# suframa.login()
data_atual = datetime.now()
ano = data_atual.strftime('%Y')
mes = data_atual.strftime('%m')
ano_mes = f'{ano}\\{mes}-{ano}'
path = os.path.join('G:\\Meu Drive\\ENCONTADORES\\[1- CENTRAL DE OBRIGACOES E ARQUIVOS]',
                    f'1 - IMPOSTOS - TRIBUTOS - TAXAS\\1 - SUFRAMA\\{ano}\\{ano_mes}')

df = pd.read_excel('senhas.xlsx', engine='openpyxl')
df['Erro'] = False
for index, row in df.iterrows():
    try:
        user = row['USUARIO']
        password = row['Senha Nova']
        suframa = Suframa(path)
        input('Enter')
        time.sleep(2)
        suframa.make_login(user, password)
        suframa.get_imprimir_gru()

        suframa.get_gru()
        suframa.select_taxa()
        suframa.download_gru()
        suframa.avancar_click()
        suframa.gerar_gru_click()

        primeiro_dia, ultimo_dia = first_lasted_day(ano, mes)
        suframa.inserir_datas(primeiro_dia, ultimo_dia)
        print('terminou')
    except Exception as e:
        df.at[index, 'Erro'] = True
        df.to_excel('resultado.xlsx', index=False)
        print(f'Erro na linha {index}: {str(e)}')

    # break
    # print(row)

    # Faça alguma ação com usuário e senha
    # suframa.fazer_alguma_acao(usuario, senha)
