# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:21:12 2023

@author: ma057659
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from math import ceil
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

"""extração automatizada de cabos usb"""
link_site = 'https://www.i2go.com.br/cabos?pagina=1'
driver = webdriver.Chrome()
driver.get(link_site)
time.sleep(2)
itens = int(driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/section[2]/div[2]/span').text)

n_paginas = ceil(itens/24)

df= pd.DataFrame({'Marca':[],'Descrição':[],'Preço':[]})

global j
j = 0
global k
k = 0
for pagina in range(1, n_paginas+1):
    link_site = link_site[0:-1] + str(pagina)
    driver.get(link_site)
    time.sleep(2)
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    
    produtos = site.find_all('div', class_='fbits-item-lista-spot')
    
    for produto in produtos:
        try:
            descricao = produto.find('h3', class_='spot-title').get_text()
        except:
            descricao = produto.find('h3', class_='spotTitle').get_text()
        try:
            preco = produto.find('span', class_='fbits-valor').get_text()
        except:
            preco = produto.find('span', class_='txt-sold-out').get_text()
        try:
            link = produto.find('a', class_='spot-info').get('href')
        except:
            link = produto.find('a', class_='spot-info hide').get('href')
        link = "https://www.i2go.com.br/" + link
        df.loc[j,'Descrição'] = descricao
        df.loc[j,'Preço'] = preco
        df.loc[j, 'Link'] = link
        j +=1
        
    for link in df['Link'][k:]:
        driver.get(link)
        time.sleep(1)
        sku = driver.find_element(By.CLASS_NAME, 'fbits-sku').text
        df.loc[k, 'SKU'] = sku
        k +=1
"""extração automatizada de carregador de celular"""

link_site = 'https://www.i2go.com.br/carregadores?pagina=1'
driver.get(link_site)
time.sleep(2)
itens = int(driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/section[2]/div[2]/span').text)

n_paginas = ceil(itens/24)

for pagina in range(1, n_paginas+1):
    link_site = link_site[0:-1] + str(pagina)
    driver.get(link_site)
    time.sleep(2)
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    
    produtos = site.find_all('div', class_='fbits-item-lista-spot')
    
    for produto in produtos:
        try:
            descricao = produto.find('h3', class_='spot-title').get_text()
        except:
            descricao = produto.find('h3', class_='spotTitle').get_text()
        try:
            preco = produto.find('span', class_='fbits-valor').get_text()
        except:
            preco = produto.find('span', class_='txt-sold-out').get_text()
        try:
            link = produto.find('a', class_='spot-info').get('href')
        except:
            link = produto.find('a', class_='spot-info hide').get('href')
        link = "https://www.i2go.com.br/" + link
        df.loc[j,'Descrição'] = descricao
        df.loc[j,'Preço'] = preco
        df.loc[j, 'Link'] = link
        j +=1
        
    for link in df['Link'][k:]:
        driver.get(link)
        time.sleep(1)
        sku = driver.find_element(By.CLASS_NAME, 'fbits-sku').text
        df.loc[k, 'SKU'] = sku
        k +=1

"""extração automatizada de carregador portátil"""

link_site = 'https://www.i2go.com.br/carregador-portatil?pagina=1'
driver.get(link_site)
time.sleep(2)
itens = int(driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/section[2]/div[2]/span').text)

n_paginas = ceil(itens/24)

for pagina in range(1, n_paginas+1):
    link_site = link_site[0:-1] + str(pagina)
    driver.get(link_site)
    time.sleep(2)
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    
    produtos = site.find_all('div', class_='fbits-item-lista-spot')
    
    for produto in produtos:
        try:
            descricao = produto.find('h3', class_='spot-title').get_text()
        except:
            descricao = produto.find('h3', class_='spotTitle').get_text()
        try:
            preco = produto.find('span', class_='fbits-valor').get_text()
        except:
            preco = produto.find('span', class_='txt-sold-out').get_text()
        try:
            link = produto.find('a', class_='spot-info').get('href')
        except:
            link = produto.find('a', class_='spot-info hide').get('href')
        link = "https://www.i2go.com.br/" + link
        df.loc[j,'Descrição'] = descricao
        df.loc[j,'Preço'] = preco
        df.loc[j, 'Link'] = link
        j +=1
        
    for link in df['Link'][k:]:
        driver.get(link)
        time.sleep(1)
        sku = driver.find_element(By.CLASS_NAME, 'fbits-sku').text
        df.loc[k, 'SKU'] = sku
        k +=1

df['SKU'] = df['SKU'].str.replace("SKU ","")
df["Marca"] = 'I2GO'
df['Descrição'] = df['Descrição'].str.strip()

#df.to_excel(r'C:\Users\ma057659\Desktop\Trabalho\Unidade de energia\Paulo\I2GO 14abr.xlsx', index=False)

df.to_excel(r'C:\Users\ma057659\Desktop\Trabalho\Unidade de energia\Paulo\Atualização de preços\I2GO.xlsx', index=False)
