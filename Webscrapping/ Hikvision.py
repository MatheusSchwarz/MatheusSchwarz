# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:28:44 2024

@author: ma057659
"""

#Importando as funções que serão utilizadas
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


#Contador
l = 0

#Criando a tabela
tabela = pd.DataFrame({"Nome da empresa":[],"Descrição":[],"Telefone":[],"Web Site":[],"Endereço":[],"Email":[]})


#Acessando o site
url = 'https://www.hikvision.com/pt-br/Partners/channel-partners/find-a-distributor/'

driver = webdriver.Chrome()
driver.get(url)

for iteracao in range(0,39):
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    
    quadradinhos = site.find_all('li', class_='cpp-item active animated slideInRight')
    
    for quadradinho in quadradinhos:
        empresa = quadradinho.find('div', class_='cpp-title').get_text()
        descricao = quadradinho.find('div', class_='cpp-description').get_text()
        tabela.loc[l,"Nome da empresa"] = empresa
        tabela.loc[l,'Descrição'] = descricao
        
        detalhe = quadradinho.find_all('li', class_='cpp-info-item')
        for item in detalhe:
            desc_detalhe = item.find('span', 'cpp-parameter').get_text()
            detalhe = item.find('span', 'cpp-details').get_text()
            tabela.loc[l,desc_detalhe] = detalhe
            print(desc_detalhe+" "+detalhe)
        l+=1
    
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/section[4]/div[1]/div[1]/a[42]').click()
    time.sleep(2)

tabela.to_excel(r'C:\Users\ma057659\Desktop\Trabalho\Greyce\Compartilhamento com a equipe\5- Webscrapping\Lista Hik.xlsx', index=False) 
    
    
