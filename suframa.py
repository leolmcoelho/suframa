import logging as log

import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pyautogui
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException


from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver

from bromo import Interation
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ocr import ocr_with_gray_filter

import os
import sys
import time
import logging
sys.path.append(os.getcwd())


os.environ['WDM_LOG'] = str(log.NOTSET)


class Suframa(Interation):

    def __init__(self):

        # options = webdriver.ChromeOptions()
        self.host = 'https://www4.suframa.gov.br/Login.aspx'
        perfil_usuario_dir = r'C:\Users\leona\AppData\Local\Google\Chrome\User Data\Profile 5'

        logging.basicConfig(filename='chromedriver.log', level=logging.WARNING)

        # service = Service(executable_path=GeckoDriverManager().install())
        service = ChromeService(executable_path='chromedriver.exe')
        options = Options()

        options.add_argument('--disable-animations')
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument(f'--user-data-dir={perfil_usuario_dir}')
        self.path = os.path.join(os.getcwd(), 'grus')
        options.add_experimental_option('prefs', {
            'download.default_directory': self.path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            "printing.print_preview_sticky_settings.enabled": False,

            "printing.print_preview_sticky_settings.printerName": "Save as PDF",

        })
        # options.page_load_strategy = 'none'
        options.add_argument('--log-level=1')

        options.add_argument('--kiosk-printing')
        options.add_argument('--disable-print-preview')
        options.add_argument('--print-to-pdf')

        # options.add_argument(r'user-data-dir={}\config\Profile 2'.format(os.getcwd()))

        self.driver = webdriver.Chrome(service=service, options=options)

        super().__init__(self.driver)
        self.url = self.host
        self.driver.get(self.url)

    def login(self, user, password, captcha=None):
        try:
            self.write('//*[@id="ContentPlaceHolder1_txtLogin"]', user)
            self.write('//*[@id="ContentPlaceHolder1_txtSenha"]', password)
            if captcha:
                self.write('//*[@id="ContentPlaceHolder1_CodigoCaptcha"]', captcha)
            # input('teste')
            self.click('//*[@id="ContentPlaceHolder1_Button1"]')
            return True
        except Exception as e:
            # print('Erro no login', e)
            pass

    def get_captcha(self, path='img'):
        try:
            time.sleep(1)
            captcha = self.element('//*[@id="ContentPlaceHolder1_Image1"]')
            if captcha:
                screenshot = captcha.screenshot_as_png
                if screenshot:
                    with open(f"{path}.png", "wb") as file:
                        file.write(screenshot)
                    return True
                else:
                    print("Erro: Captura de tela do elemento não está disponível.")
                    return False
            else:
                print("Erro: Elemento não encontrado.")
                return False
        except Exception as e:
            # print(f"Erro ao capturar o captcha: {str(e)}")
            return True

    def pass_captcha(self, img='img.png'):

        self.get_captcha()
        text = ocr_with_gray_filter(img)
        print('resultado do captcha', text)
        if text:
            # Excluir o arquivo de imagem após a leitura
            try:
                pass
                # os.remove(img)
                # print(f'Arquivo {img} excluído com sucesso.')
            except Exception as e:
                print(f'Erro ao excluir o arquivo {img}: {str(e)}')

            return text

    def tratar_alert(self):
        try:
            alert = self.driver.switch_to.alert
            if alert:
                self.driver.refresh()
                return False
            else:
                return True
        except Exception as e:
            # print(f"Erro alert: {str(e)}")
            pass

    def get_gru(self):
        self.driver.get('https://www4.suframa.gov.br/arrecadacao/Gru/Gru_Gerar.aspx')

    def select_taxa(self, option='TCIF'):
        self.select_option('//*[@id="ContentPlaceHolder1_dropTipoTaxa"]', text=option)

    def verify_login(self):
        # Verfica se fez o login ou nao
        'se nao tiver /login na url ele da true'
        try:

            url_em_minusculas = self.driver.current_url.lower()
            if "login" in url_em_minusculas:
                return False
            else:
                return True
        except Exception as e:
            pass

        return False

    def check_alert_captcha(self):
        # self.wait.until(EC.alert_is_present())
        try:
            try:
                wait = WebDriverWait(self.driver, 5)
                alert = wait.until(EC.alert_is_present())
                print("Alerta encontrado. Texto do alerta:", alert.text)
            except:
                pass
            # print("Alerta encontrado. Texto do alerta:", alert.text)
            if 'imagem não confere!' not in alert.text:
                # print("Texto do alerta:", alert.text)
                return True
            # print("Alerta encontrado. Texto do alerta:", alert.text)
            # Faça algo com o alerta, por exemplo, aceite-o
            # alert.accept()
            return False
        except Exception as e:
            # print("Nenhum alerta encontrado dentro do prazo de espera.")
            return False

    def tratar_mes(self, date):
        data_atual = datetime.now()
        date = date.split('/')[1]
        mes = data_atual.strftime('%m')
        if date == mes:
            return True

    def download_gru(self):

        try:
            # //*[@id="ContentPlaceHolder1_gridSolicitacaoGrupo"]/tbody/tr[5]/td[3]
            elements = len(self.elements('//tr/td/span')) + 1
        except:
            print(False)
            return False
        # print(elements)

        for i in range(2, elements):

            try:

                # print(i.get_attribute('outerHTML'))
                # input_i = i.find_i('xpath', '//input')
                # print(f'//tr[{i}]/td/span/input')
                path_date = f'//tr[{i}]/td[3]'
                data = self.element(path_date).text
                if self.tratar_mes(data):
                    self.click(f'//tr[{i}]/td/span/input')
                    time.sleep(1)
                    try:
                        self.click('//*[@id="ContentPlaceHolder1_gridvisualisar_chkAllRow"]')
                    except Exception as e:
                        pass
                        # print(e)
                        # print('click no box falhou, item', i)
                    # print('item ', i)
                    time.sleep(1)
            except StaleElementReferenceException:
                # Captura a exceção e lida com isso aqui, se um elemento estiver "stale"
                print(f"Elemento {i} não está mais no DOM.")

        return True

    def avancar_click(self):
        self.click('//*[@id="ContentPlaceHolder1_LinkButton2"]')

    def gerar_gru_click(self, name, destino):
        self.click('//*[@id="ContentPlaceHolder1_lbGerarGru"]')
        try:
            el = self.element('//*[@id="ContentPlaceHolder1_lbOk"]', 3)
            el.click()
        except:
            el = False

        if not el:
            self.click('//*[@id="ContentPlaceHolder1_lbImprimir"]')          
            self.change_name_boleto(name)
            self.change_path_boleto(name, self.path, destino)
            
            
    def change_path_boleto(self, arquivo, pasta_origem, pasta_destino):
        try:
            # Monta o caminho completo do arquivo de origem
            caminho_origem = os.path.join(pasta_origem, f'{arquivo}.pdf')

            # Monta o caminho completo do arquivo de destino
            caminho_destino = os.path.join(pasta_destino, f'{arquivo}.pdf')

            # Move o arquivo
            shutil.move(caminho_origem, caminho_destino)

            print(f"O arquivo '{arquivo}.pdf' foi movido de '{pasta_origem}' para '{pasta_destino}'.")
        except Exception as e:
            print(f"Erro ao mover o arquivo: {str(e)}")
    

    def change_name_boleto(self, name):
        
        arquivos = os.listdir(self.path)
        pdfs = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.pdf')]
        
        if not pdfs:
            print("Nenhum arquivo PDF encontrado na pasta de origem.")
            return
        
        arquivo_pdf = pdfs[0]
        novo_nome_pdf = os.path.join(self.path, name + '.pdf')
        
        os.rename(os.path.join(self.path, arquivo_pdf), novo_nome_pdf)
        
        
        
    def get_imprimir_gru(self):
        self.driver.get(
            'https://www4.suframa.gov.br/arrecadacao/Gru/ConsultarUsuarioExterno/ConsultarUsuarioExterno.aspx')

    def inserir_datas(self, initial_date, final_date, name):
        self.select_option('//*[@id="ContentPlaceHolder1_DropDownPeriodo"]', '2')
        time.sleep(0.5)
        self.write('//*[@id="txtDtInicio"]', initial_date)
        self.write('//*[@id="txtDtFim"]', final_date)
        try:
            self.select_option('//*[@id="ContentPlaceHolder1_DropDownTipoTaxa"]', '1')
            self.select_option('//*[@id="ContentPlaceHolder1_DropDownSitGru"]', '0')

            self.click('//*[@id="ContentPlaceHolder1_pesquisarGru"]')

            self.click('//*[@id="ContentPlaceHolder1_gridGRU_linkExtrato_0"]')

            self.imprimir(name)
            
            return True

        except:
            return False

    def imprimir(self, name):
        print(name)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.typewrite(name)
        pyautogui.press('enter')


    def make_login(self, user, password, tentativas=10):

        # login code 1
        # terminou as tentativas code 2
        if not self.verify_login():
            # return True
            captcha = self.pass_captcha()
            self.login(user, password, captcha)

            print('resultado do captcha', captcha)

            for _ in range(tentativas):

                if self.check_alert_captcha():
                    return True

                if self.verify_login():
                    return 'fez login'
                captcha = self.pass_captcha()

                self.login(user, password, captcha)
                if self.verify_login():
                    return 'fez login'

                time.sleep(5)

            if self.verify_login():
                return 'fez login'
            print('terminou o for')

            return 'pausa'


if __name__ == '__main__':
    # user, senha = ()
    # print(os.getcwd())
    # os.system('cls')
    print('start')
    data_atual = datetime.now()
    ano = data_atual.strftime('%Y')
    mes = data_atual.strftime('%m')
    ano_mes = f'{ano}\\{mes}-{ano}'
    path = os.path.join(os.getcwd(),
                        f'1 - IMPOSTOS - TRIBUTOS - TAXAS\\1 - SUFRAMA\\{ano}\\{ano_mes}')

    user = '09642884000152'
    password = 'Portal2022'

    s = Suframa(path)
    # s.login(user, password)
    login = s.make_login(user, password, 10)
    if login:
        if login == 'pausa':
            start_time = time.time()
            while True:
                if s.verify_login():
                    break

                elapsed_time = time.time() - start_time
                if elapsed_time >= 5*60:  # 300 segundos = 5 minutos
                    print("Tempo limite de 5 minutos atingido. Saindo do loop.")
                    break
                time.sleep(5)

        elif login != 'fez login':
            print('Login errado ou acabou as tentativas')
            time.sleep(5)

    # captcha = s.pass_captcha()
    # print('resultado do captcha', captcha)

    os.system('cls')
    print('saiu do captcha')
    # s.get_gru()
    # s.select_taxa()

    # if s.download_gru():
    # pass
#        s.avancar_click()
        #s.gerar_gru_click()

    s.get_imprimir_gru()
    s.inserir_datas('01/10/2023', '31/10/2023', path)

    try:

        pass

    except Exception as e:
        tb_info = traceback.format_exc()
        mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"

        print(mensagem_erro)
    finally:
        input('sair')
        s.driver.close()
