from selenium import webdriver
import time
import pytz #libreria para la timezone de todo el mundo
from datetime import datetime
from models.containers import cont as container
tz_bsas = pytz.timezone('America/Argentina/Buenos_Aires') #timezone de argentina
listaDeHorarios = [] #Guarda los horarios que scrappea
listaMantieneHorarios = [] #Mantiene los horarios de todo el dia
d=0

options = webdriver.FirefoxProfile("C:/Users/fotos/AppData/Roaming/Mozilla/Firefox/Profiles/69cvsut4.default-release/") 
driver = webdriver.Firefox(executable_path="./geckodriver.exe",firefox_profile=options)

def getTimes():
    driver.get("https://drive.google.com/drive/folders/1NFzSZkVNK3RSibLfA33dsIjLflQhQo04")
    time.sleep(7)

    if driver.find_element_by_class_name(container.contHoy).text == "Hoy": #Container donde dice la fecha
        logs = driver.find_elements_by_class_name(container.contLogs)
        for elem2 in logs[:10]: #Container de cada log en drive
            elem3 = elem2.find_element_by_class_name(container.contHora) #Container de la hora
            datetime_bsas = datetime.now(tz_bsas) #guarda la fecha actaual (now) de buenos aires
            dia = datetime_bsas.strftime("%d") #formatea la fecha en el formato de solo "DD" porque no quiero que me muestre mas que el dia
            if (elem3.get_attribute("title"))[0:2]==dia:
                print(elem3.get_attribute("title"))
                listaDeHorarios.append(elem3.get_attribute("title"))
    else:
        listaDeHorarios.clear()

while True:
    getTimes()
    print("--------------------------")
    if listaMantieneHorarios:
        c= -1
        objHoraScreenshot = driver.find_elements_by_class_name(container.contLogs) #Busca en los container de los logs
        for x in listaDeHorarios:
            c +=1
            if x not in listaMantieneHorarios:
                d += 1
                objHoraScreenshot[c].screenshot("./imgs/{f}-imagen.png".format(f=d))
                listaMantieneHorarios.insert(0,x)
                if len(listaMantieneHorarios)>10:listaMantieneHorarios.pop()
                print(x,"IMAGEN GUARDADA")
        #listaMantieneHorarios.sort()
        listaDeHorarios.clear()
    else:
        print("ESTOY EN EL ELSE")
        listaMantieneHorarios=listaDeHorarios.copy()
        
    listaDeHorarios.clear()
    #listaMantieneHorarios.sort()
    print(listaMantieneHorarios , "##listaDeHorarios vieja")
    print(listaDeHorarios, "##listaDeHorarios nueva, se supone que debería estar vacia")

    #NOTAS:
    '''
    YA ESTA CASI TODO TERMINADO, EL ARRAY SE VA A LLENAR CON LOS ULTIMOS 15 ELEMENTOS (SI HAY 15, SINO MENOS, PERO AGUANTA HASTA 15)
    LO QUE FALTA ES HACER QUE EL PROGRAMA AL FINAL, SI YA HAY 15 HORARIOS Y SE SUMA UNO AL ARRAY (O SEA QUEDAN 16) SE BORRE EL ULTIMO,
    (EL QUE FUE AGREGADO EN PRIMER LUGAR, O SEA EL MAS VIEJO)
    '''