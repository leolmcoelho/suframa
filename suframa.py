import logging as log
import pickle
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pyautogui
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException


from selenium.webdriver.firefox.service import Service as GeckoService

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import datetime
from bromo import Interation

from ocr import ocr_with_gray_filter

import os
import sys
import time
import logging
sys.path.append(os.getcwd())


os.environ['WDM_LOG'] = str(log.NOTSET)


class Suframa(Interation):

    def __init__(self, path):

        # options = webdriver.ChromeOptions()
        self.host = 'https://www4.suframa.gov.br/Login.aspx'
        # perfil_usuario_dir = r'C:\Users\leona\AppData\Local\Google\Chrome\User Data\Profile 5'

        logging.basicConfig(filename='chromedriver.log', level=logging.WARNING)

        # service = Service(executable_path=GeckoDriverManager().install())
        service = ChromeService(executable_path='chromedriver.exe')
        options = Options()

        options.add_argument('--disable-animations')
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument(f'--user-data-dir={perfil_usuario_dir}')
        options.add_experimental_option('prefs', {
            'download.default_directory': path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,  # Isso desativa a verificação de segurança, use com cautela,
            "printing.print_preview_sticky_settings.enabled": False,

            "printing.print_preview_sticky_settings.printerName": "Save as PDF"
        })
        # options.page_load_strategy = 'none'
        options.add_argument('--log-level=1')

        options.add_argument('--kiosk-printing')
        options.add_argument('--disable-print-preview')
        options.add_argument('--print-to-pdf')

        # options.add_argument(r'user-data-dir={}\config\Profile 2'.format(os.getcwd()))

        self.driver = webdriver.Chrome(service=service, options=options,
                                       service_log_path='chromedriver.log')

        super().__init__(self.driver)
        self.url = self.host
        self.driver.get(self.url)

    def login(self, user, password, captcha):

        # time.sleep(1)
        try:
            self.write('//*[@id="ContentPlaceHolder1_txtLogin"]', user)
            self.write('//*[@id="ContentPlaceHolder1_txtSenha"]', password)

            self.write('//*[@id="ContentPlaceHolder1_CodigoCaptcha"]', captcha)
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
                os.remove(img)
                print(f'Arquivo {img} excluído com sucesso.')
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

    def verify_captcha(self):
        try:
            url_em_minusculas = self.driver.current_url.lower()

    # Verifica se a palavra "login" está na URL
            if "login" in url_em_minusculas:
                return False
            else:
                return True
        except Exception as e:
            pass

    def download_gru(self):

        elements = len(self.elements('//tr/td/span')) + 2
        print(elements)

        for i in range(2, elements):

            try:

                # print(i.get_attribute('outerHTML'))
                # input_i = i.find_i('xpath', '//input')
                print(f'//tr[{i}]/td/span/input')
                self.click(f'//tr[{i}]/td/span/input')
                time.sleep(1)
                try:
                    self.click('//*[@id="ContentPlaceHolder1_gridvisualisar_chkAllRow"]')
                except Exception as e:
                    print(e)
                    print('click no box falhou, item', i)
                print('item ', i)
                time.sleep(1)
            except StaleElementReferenceException:
                # Captura a exceção e lida com isso aqui, se um elemento estiver "stale"
                print(f"Elemento {i} não está mais no DOM.")

    def avancar_click(self):
        self.click('//*[@id="ContentPlaceHolder1_LinkButton2"]')

    def gerar_gru_click(self):
        self.click('//*[@id="ContentPlaceHolder1_lbGerarGru"]')
        self.click('//*[@id="ContentPlaceHolder1_lbImprimir"]')

    def get_imprimir_gru(self):
        self.driver.get(
            'https://www4.suframa.gov.br/arrecadacao/Gru/ConsultarUsuarioExterno/ConsultarUsuarioExterno.aspx')

    def inserir_datas(self, initial_date, final_date):
        self.select_option('//*[@id="ContentPlaceHolder1_DropDownPeriodo"]', '2')
        time.sleep(0.5)
        self.write('//*[@id="txtDtInicio"]', initial_date)
        self.write('//*[@id="txtDtFim"]', final_date)

        self.select_option('//*[@id="ContentPlaceHolder1_DropDownTipoTaxa"]', '1')
        self.select_option('//*[@id="ContentPlaceHolder1_DropDownSitGru"]', '0')

        self.click('//*[@id="ContentPlaceHolder1_pesquisarGru"]')

        self.click('//*[@id="ContentPlaceHolder1_gridGRU_linkExtrato_0"]')

        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.typewrite('extrato')
        pyautogui.press('enter')

    def make_login(self, user, password):
        if not self.verify_captcha():
            captcha = self.pass_captcha()
            print('resultado do captcha', captcha)
            self.login(user, password, captcha)
            while True:

                if self.verify_captcha():
                    break
                alert = self.tratar_alert()

                if alert:
                    break
                time.sleep(1)
                captcha = self.pass_captcha()

                self.login(user, password, captcha)
                if self.verify_captcha():
                    break


if __name__ == '__main__':
    # user, senha = ()
    # print(os.getcwd())
    # os.system('cls')
    print('start')
    data_atual = datetime.datetime.now()
    ano = data_atual.strftime('%Y')
    mes = data_atual.strftime('%m')
    ano_mes = f'{ano}\\{mes}-{ano}'
    path = os.path.join(os.getcwd(),
                        f'1 - IMPOSTOS - TRIBUTOS - TAXAS\\1 - SUFRAMA\\{ano}\\{ano_mes}')

    user = '5910245000250'
    password = 'carga2023'

    s = Suframa(path)
    s.make_login(user, password)
    # captcha = s.pass_captcha()
    # print('resultado do captcha', captcha)

    os.system('cls')
    print('saiu do captcha')
    # s.get_gru()
    # s.select_taxa()

    # s.download_gru()
    # s.avancar_click()
    # s.gerar_gru_click()

    s.get_imprimir_gru()
    s.inserir_datas('01/10/2023', '31/10/2023')

    try:

        pass

    except Exception as e:
        tb_info = traceback.format_exc()
        mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"

        print(mensagem_erro)
    finally:
        input('sair')
        s.driver.close()
