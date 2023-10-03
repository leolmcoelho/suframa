import os
from suframa import Suframa
import pandas as pd
import time
from date import *

import calendar

from datetime import datetime


# suframa.login()

path = make_path()

dtype_dict = {'USUARIO': str}
df = pd.read_excel('senhas.xlsx', engine='openpyxl', dtype=dtype_dict)
df['Erro'] = False
for index, row in df.iterrows():
    try:
        user = row['USUARIO']
        password = row['Senha Nova']
        
        paste = row['Pasta']
        
        empresa = row['Razão Social']

        print('usuário: ', user)
        
        path = os.path.join(path, paste)
        suframa = Suframa()
        # input('Enter')
        time.sleep(2)
        login = suframa.make_login(user, password, 3)
        if login:
            
            if login == 'pausa':
                start_time = time.time()
                timeout = False
                while True:
                    if suframa.verify_login():
                        break
                    
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 5*60:  # 300 segundos = 5 minutos
                        print("Tempo limite de 5 minutos atingido. Saindo do loop.")
                        timeout = True
                        break
                       
                if timeout:
                    continue
                time.sleep(5)
                
            elif login != 'fez login': 
                print('Login errado ou acabou as tentativas')
                time.sleep(5)
                continue
            
        suframa.get_gru()
        suframa.select_taxa()

        if suframa.download_gru():
            suframa.avancar_click()
            suframa.gerar_gru_click()
        
        suframa.get_imprimir_gru()

        suframa.get_gru()
        suframa.select_taxa()
        
        if suframa.download_gru():
            suframa.avancar_click()
            suframa.gerar_gru_click()
        
        suframa.get_imprimir_gru()

        primeiro_dia, ultimo_dia = first_lasted_day(ano, mes)
        
        ano, mes, _ = day_now()
        
        nome = f'{mes}-{ano} Extrato Suframa - {empresa}'
        create_dir(path)
        
        if suframa.inserir_datas(primeiro_dia, ultimo_dia, nome):
            df.at[index, 'Erro'] = 'Sem registro'
            df.to_excel('resultado.xlsx', index=False)
            continue
        
        
        print('terminou')
    except Exception as e:
       df.at[index, 'Erro'] = True
       df.to_excel('resultado.xlsx', index=False)
       print(e)
    # print(f'Erro na linha {index}: {str(e)}')
