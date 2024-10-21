# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:14:54 2023

@author: ma057659
"""

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from math import ceil
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


#NÃO FUNCIONA MAIS, O SITE ATUALIZOU

termo_procurado = 'power bank'
termo_procurado = termo_procurado.replace(" ","%20")

url = 'https://www.elgstore.com.br/'+"produto?q="+termo_procurado

df = pd.DataFrame({'Marca':[], 'Descrição':[], 'Preço':[], 'Código Produto':[]})

driver = webdriver.Chrome()
driver.get(url)
time.sleep(4)


html = driver.page_source
site = BeautifulSoup(html, 'html.parser')

produtos = site.find_all('a', class_='grid__cardLink')

global j
j = 0

for produto in produtos:
    nome_produto = produto.find('a', class_='product-name').get_text()
    try:
        preco = produto.find('div', class_='price').get_text()
        preco = preco.strip().replace("R$ ",'')
        df.loc[j,'Preço'] = preco
    except:
        df.loc[j, 'Preço'] = 'Sem preço'
    link = produto.find('a', class_='product-name').get('href')
    link = 'https:' + link
    df.loc[j,'Marca'] = 'ELG'
    df.loc[j,'Descrição'] = nome_produto
    df.loc[j,'Link'] = link
    j += 1

while True:
    try:
        for i in range(0,10):
            driver.find_element(By.XPATH, '//*[@id="PagerBottom_16146058"]/ul/li[8]').click()
            html = driver.page_source
            site = BeautifulSoup(html, 'html.parser')
            produtos = site.find_all('div', class_='article__body') 
            for produto in produtos:
                nome_produto = produto.find('a', class_='product-name').get_text()
                try:
                    preco = produto.find('div', class_='price').get_text()
                    preco = preco.strip().replace("R$ ",'')
                    df.loc[j,'Preço'] = preco
                except:
                    df.loc[j, 'Preço'] = 'Sem preço'
                link = produto.find('a', class_='product-name').get('href')
                link = 'https:' + link
                df.loc[j,'Marca'] = 'ELG'
                df.loc[j,'Descrição'] = nome_produto
                df.loc[j,'Link'] = link
                j += 1
            time.sleep(2)
        break
    except:
        break
    
    

df['Código Produto'] = (df['Descrição'] + " - nada").str.split("- ")
df['Código Produto'] = df['Código Produto'].str[-2]
df['Código Produto'] = df['Código Produto'].str.strip()

"""df1 = pd.DataFrame()
k = 0
for link in df['Link']:
    try:
        driver.get(link)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/section[2]/div/div/div[1]/div/div/div/div[2]/div[1]').click()
        time.sleep(1)
        caracteristicas = driver.find_element(By.XPATH, '//*[@id="app"]/section[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/ul[1]').text
        caracteristicas = caracteristicas.split('\n')
        caracteristicas = pd.Series(caracteristicas)
        caracteristicas = caracteristicas.str.split(":")
        colunas = [caracteristica[0] for caracteristica in caracteristicas]
        valores = [caracteristica[1] for caracteristica in caracteristicas]
        caracteristicas = pd.DataFrame({'Característica':colunas, 'Descrição':valores}).T
        caracteristicas.columns = colunas
        caracteristicas = caracteristicas.drop('Característica', axis=0)
        caracteristicas.reset_index(drop=True, inplace=True)
        df1 = df1.append(caracteristicas, ignore_index=True)
        df1.loc[k, 'Index'] = k
        k +=1
    except:
        k +=1
    
df.reset_index(inplace=True)

resultado = df.join(df1, how='left', on='index')
resultado = resultado.drop(['index','Index'], axis=1)"""

""" etapa de tratamento do df obtido"""
string = df['Código Produto']
string1 = string.str.split()
m = 0
teste = pd.DataFrame({})
for elemento in string1:
    try:
        string2 = ' '.join([ele for ele in elemento if ele.isupper()])
        teste.loc[m, 'filtro'] = string2
        m +=1
    except:
        m +=1
        
teste['filtro'] = teste['filtro'].str.replace(',',' +').str.replace("'","").str.strip()
df['Código Produto'] = teste['filtro']

df.to_excel(r'C:\Users\ma057659\Desktop\Trabalho\Unidade de energia\Paulo\Atualização de preços\power bank ELG.xlsx', index=False)
