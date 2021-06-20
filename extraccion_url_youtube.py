#%%
from time import sleep, time
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


marcio = webdriver.Chrome('./chromedriver')

archivo_excel = pd.ExcelFile('letras_de_canciones.xlsx')
df=archivo_excel.parse()
lista_url_yb = []

constante ='lyrics'
marcio.get('https://www.youtube.com')
sleep(2)
for nombre in df['title'][683:]:
    #a = marcio.find_elements_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input')
    marcio.find_element_by_name("search_query").clear()
    sleep(1)
    a = marcio.find_element_by_name("search_query")
    boton = marcio.find_element_by_id("search-icon-legacy")
    const =nombre + ' ' +constante
    a.send_keys(const)
    sleep(1)
    boton.click()
    sleep(3)
    musica =marcio.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]")
    musica.click()
    sleep(3)
    #extraer link youtube  de la pagina actual
    lista_url_yb.append(marcio.current_url)
    sleep(1)
    
    #marcio.close()

#%%
df['youtube'] = lista_url_yb

#guarda el dataframe en un excel
writer = pd.ExcelWriter('letras_de_canciones2.xlsx')
df.to_excel(writer, 'principal')
writer.save()
writer.close()

# %%
