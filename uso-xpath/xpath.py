from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://www.booking.com/')
time.sleep(3)
#pulsamos el botón de aceptar cookies
boton_aceptar = driver.find_elements(By.XPATH,"//*[@id='onetrust-accept-btn-handler']")
boton_aceptar[0].click()

#en el input a donde desea ir incluimos el destino
destino = driver.find_elements(By.XPATH,"//form/div/div/div/div/div/div/div/input")
destino[0].send_keys('Disneyland Paris')

time.sleep(1)

#pulsamos el botón buscar
boton = driver.find_elements(By.XPATH,"//form/div/div[4]/button")
boton[0].click()

time.sleep(3)

#si nos sale el cuadro de dialogo para darnos de alta como genius lo cerramos
boton_cerrar = driver.find_elements(By.XPATH,"//*[@aria-label='Ignorar información sobre el inicio de sesión.']")
boton_cerrar[0].click()
                                    
i = 1
tarjeta = driver.find_elements(By.XPATH,"//div[@data-testid='property-card-container']")
client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True) 

db = client['travel']
collection = db['destinos']


for elem in tarjeta:
    nombre = elem.find_elements(By.XPATH,"div[2]/div/div/div/div/div/div/h3/a/div")
    print('Nombre: ' + nombre[0].text)

    imagen = elem.find_elements(By.XPATH,"div[1]/div/a/img")
    print('Imagen: ' + imagen[0].get_attribute('src'))

    url = elem.find_elements(By.XPATH,"div[2]/div/div/div/div/div/div/h3/a") 
    print('url: ' + url[0].get_attribute('href')) 

    driver2 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver2.get(url[0].get_attribute('href'))
    time.sleep(3)

    boton_cookie = driver2.find_elements(By.XPATH,"//*[@id='onetrust-accept-btn-handler']")
    boton_cookie[0].click()

    servicios = driver2.find_elements(By.XPATH,"//*[@id='basiclayout']/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/ul/li")
    if not servicios:
        servicios = driver2.find_elements(By.XPATH,"//*[@id='basiclayout']/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/div/ul/li")
    lista_servicios = []
    for s in servicios:
        s_e = s.find_elements(By.XPATH,"div/div/div/span/div/span")
        if s_e:
            lista_servicios.append(s_e[0].text)
    delimiter = ","
    #concatenamos la lista en array
    lista_servicios_string = delimiter.join(lista_servicios)
    print('servicios: ' + lista_servicios_string)

    descripcion = driver2.find_elements(By.XPATH,"//*[@id='basiclayout']/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/div/p[1]")
    if descripcion:
        desc = descripcion[0].text
    else:
        desc = ""

    hotel_info = {'nombre':'DISNEYLAND PARIS ' + str(i) , 'hotel':nombre[0].text, 'resumen':desc, 'servicios':lista_servicios_string, 
           'img':imagen[0].get_attribute('src'), 'teaser':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7eh4u7gEevYIXHg0UDbODzmXLDu6bWAgPyg&s'}
    i += 1
    print(hotel_info)
    collection.insert_one(hotel_info)

    driver2.close()
