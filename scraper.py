from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# URL da NASA Exoplanet
START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(START_URL)

time.sleep(10)

planets_data = []

# Defina o método de coleta de dados dos exoplanetas
def scrape():

    for i in range(0,25):
        print(f'Coletando dados da página {i+1} ...' )
        pegaDados = BeautifulSoup(browser.page_source,"html.parser")

        for i in pegaDados.find_all("ul",attrs={"class","exoplanet"}):
            encontraDados = i.find_all("li")
            print(encontraDados)
            temp_planetas=[]
            for index, conteudo in enumerate(encontraDados):
                if index==0:
                    nome = conteudo.find_all("a")[0].contents[0]
                    temp_planetas.append(nome)
                else:
                    try:
                        temp_planetas.append(conteudo.contents[0])
                    except:
                        temp_planetas.append("")
            planets_data.append(temp_planetas)
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        
# Chamando o método   
scrape()

# Defina o cabeçalho
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Defina o dataframe do pandas   
planetas = pd.DataFrame(planets_data,columns=headers)

# Converta para CSV
planetas.to_csv("planetas.csv",index=True,index_label="id")
    


