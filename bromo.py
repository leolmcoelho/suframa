import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


class Interation:
    
    #wait = WebDriverWait(self.driver, time)
    def __init__(self, driver, time = 10):
        self.wait = WebDriverWait(self.driver, time)
        self.driver = driver

    
    #def write(self, tag:str, message:str, method:str='xpath', time:int=15):
            
            #WebDriverWait(self.driver, time).until(
            #        EC.element_to_be_clickable((method, tag)))
            #element = self.driver.find_element(method, tag)
                        
           # element.send_keys(str(message))
           # return True
                        

    def click(self, tag:str, method = 'xpath', time=10):
            el = WebDriverWait(self.driver, time).until(
                    EC.element_to_be_clickable((method, tag)))
            self.driver.execute_script("arguments[0].click();", el)
                
            return True
        
    
    def key(self, tag:str, key = 'enter',  time:int=15, method:str='xpath'):
                                
        WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((method, tag)))
        element = self.driver.find_element(method, tag)
                            
        actions = {
            'enter': Keys.ENTER,
            'esc': Keys.ESCAPE,
            'down': Keys.DOWN,
            'home': Keys.HOME,
            'tab': Keys.TAB
        }
        
        if key in actions:
            element.send_keys(actions[key])
        else:
            element.send_keys(key)
            
        
        return True
    
    
    def element(self, tag:str, time:int=15, method:str='xpath'):
        
        WebDriverWait(self.driver, time).until(
                EC.element_to_be_clickable((method, tag)))
        element = self.driver.find_element(method, tag)
        
        return element
    
    
    def elements(self, tag:str, time:int=15, method:str='xpath'):
        
        WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((method, tag)))
        elements = self.driver.find_elements(method, tag)
        
        return elements
    
    def locacated(self, tag:str, time:int=15, method:str='xpath'):
        if self.element(tag, time, method):
            return True
    
        else:
            return False
    
    
    def get_attribute(self, tag:str, attribute:str='value', time:int=15, method:str='xpath'):
    
        return self.element(tag, time, method).get_attribute(attribute)
        
        
    def click_js(self, tag:str,time:int=15, method:str='xpath'):
        el = self.element(tag, time, method)
        self.driver.execute_script("arguments[0].click();", el)
       
    
    def verify_page(self, param, time_break = 10):
        initial = time.time()
        
        while time.time() - initial < time_break:
            url = self.driver.current_url
        
            url =  url.split('/')
            if param in url:
                return True
        
        return False
    

    def write_js(self, tag, value ):
        js = f'document.querySelector("{tag}").value = "{value}"'
        self.driver.execute_script(js)
        
    def write(self, selector, value:str, time=15, method='xpath'):
        el = self.element(selector, time, method)
        #self.driver.execute_js("arguments[0].value = arguments[1];", el, value)
        el.send_keys(str(value))
        
    
    def cel(self, texto:str):
        number = re.findall(r'\d+', texto)
        number = ''.join(number)
        number = str(int(number))
        if len(number) != 11:
            raise ValueError("O número de celular informado é inválido. Verifique se o número tem exatamente 11 dígitos.")
        celular = number[2:]
        ddd = number[:2] 
        
        return ddd, celular
    
    
    def select_option(self, tag: str, value: str = None, text: str = None, time: int = 15, method: str = 'xpath'):
        
        select_element = self.element(tag, time, method)
        select = Select(select_element)

        if value:
            select.select_by_value(value)
            return True

        if text:
            select.select_by_visible_text(text)
            return True

        return False
    
if __name__ == '__main__':
    def main(test:str):
        if type(test) == str:
            print('é bool')
        print(type(test))
        
        print('é boll' + test)
        
    main(True)
    