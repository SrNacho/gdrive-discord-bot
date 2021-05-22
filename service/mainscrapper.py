from dotenv import load_dotenv
from selenium import webdriver
import time
import dotenv
import os
import sys
sys.path.append('..\scrapper de drive\\models')
import pytz #libreria para la timezone de todo el mundo
from datetime import datetime
from containers import cont

load_dotenv()
URL = os.getenv('DRIVE_URL')
TIME_ZONE = os.getenv('TIME_ZONE')
MOZILLA_PROFILE = os.getenv('PROFILE')

class bot:
    d=0
    tz_bsas = pytz.timezone(TIME_ZONE) #timezone de argentina
    listaDeHorarios = [] #Guarda los horarios que scrappea
    listaMantieneHorarios = [] #Mantiene los horarios de todo el dia
    container = cont()
    options = webdriver.FirefoxProfile(MOZILLA_PROFILE) 
    driver = webdriver.Firefox(executable_path="./geckodriver.exe",firefox_profile=options)

    def getTimes(self):
        self.driver.get(URL)
        time.sleep(7)
        if self.driver.find_element_by_class_name(self.container.contHoy).text == "Hoy": #Container donde dice la fecha
            logs = self.driver.find_elements_by_class_name(self.container.contLogs)
            for elem2 in logs[:10]: #Container de cada log en drive
                elem3 = elem2.find_element_by_class_name(self.container.contHora) #Container de la hora
                datetime_bsas = datetime.now(self.tz_bsas) #guarda la fecha actaual (now) de buenos aires
                dia = datetime_bsas.strftime("%d") #formatea la fecha en el formato de solo "DD" porque no quiero que me muestre mas que el dia
                if (elem3.get_attribute("title"))[0:2]==dia:
                    #print(elem3.get_attribute("title"))
                    self.listaDeHorarios.append(elem3.get_attribute("title"))
        else:
            self.listaDeHorarios.clear()
        
    def start(self):
        while True:            
            self.getTimes()
            print("--------------------------")
            if self.listaMantieneHorarios:
                c= -1
                objHoraScreenshot = self.driver.find_elements_by_class_name(self.container.contLogs) #Busca en los container de los logs
                for x in self.listaDeHorarios:
                    c +=1
                    if x not in self.listaMantieneHorarios:
                        self.d += 1
                        objHoraScreenshot[c].screenshot("./imgs/{f}-imagen.png".format(f=self.d))
                        self.listaMantieneHorarios.insert(0,x)
                        if len(self.listaMantieneHorarios)>10:self.listaMantieneHorarios.pop()
                        return 200
                        #print(x,"IMAGEN GUARDADA")
                #listaMantieneHorarios.sort()
                self.listaDeHorarios.clear()
            else:
                #print("ESTOY EN EL ELSE")
                self.listaMantieneHorarios=self.listaDeHorarios.copy()
                
            self.listaDeHorarios.clear()
            #listaMantieneHorarios.sort()
            #print(self.listaMantieneHorarios , "##listaDeHorarios vieja")
            #print(self.listaDeHorarios, "##listaDeHorarios nueva, se supone que debería estar vacia")

            #NOTAS:
            '''
            YA ESTA CASI TODO TERMINADO, EL ARRAY SE VA A LLENAR CON LOS ULTIMOS 15 ELEMENTOS (SI HAY 15, SINO MENOS, PERO AGUANTA HASTA 15)
            LO QUE FALTA ES HACER QUE EL PROGRAMA AL FINAL, SI YA HAY 15 HORARIOS Y SE SUMA UNO AL ARRAY (O SEA QUEDAN 16) SE BORRE EL ULTIMO,
            (EL QUE FUE AGREGADO EN PRIMER LUGAR, O SEA EL MAS VIEJO)
            '''