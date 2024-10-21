# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 20:25:22 2023

@author: metma
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from math import ceil
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

termo_procurado = str(input('\nO que você quer pesquisar na Kalunga?\n'))

df = pd.DataFrame({'Marca':[], 'Descrição':[], 'Preço':[]})

while True:    
    try:
        salvar_excel = str(input('Insira o endereço onde você deseja salvar o arquivo: '))+ '\\'
        salvar_excel = salvar_excel.replace('\\','/')
        nome_arquivo = str(input('insira o nome do arquivo que deseja salvar: '))
        df.to_excel(salvar_excel+nome_arquivo+'.xlsx')
        break
    except:
        print('Por favor, insira um endereço e/ou nome de arquivo válido')

print('Operação em andamento. Por favor, aguarde. Uma janela do navegador irá abrir para efetuar a coleta.')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
driver = webdriver.Chrome()
driver.get('https://www.kalunga.com.br/busca/1?q='+termo_procurado)

try:
    quantidade_produtos = int(driver.find_element(By.XPATH, '//*[@id="page-busca"]/div[2]/div[1]/div/div/div/p[2]/span[1]').text)
except:
    print('a Kalunga não vende esse produto. Também há a possibilidade da página estar formatada diferente para essa busca, tente mudar a palavra chave. Será retornado um erro de execução do código')
paginas = ceil(quantidade_produtos / 50)

global j
j = 0
for pagina in range(1,paginas+1):
    if paginas == 1:
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')        
    else:
        cabecalho = driver.find_elements(By.CLASS_NAME, 'page-item')
        cabecalho[pagina].click()
        time.sleep(2)
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')

    produtos = site.find_all('div', class_='col-12 col-sm-8 col-md-12 px-1 px-sm-3 d-flex flex-column justify-content-between')

    for produto in produtos:
        nome = produto.find('a', class_='blocoproduto__link').get_text().strip()       
        link = 'https://kalunga.com.br' + produto.find('a', class_='blocoproduto__link').get('href')
        df.loc[j, 'Link'] = link
        response = requests.get(link, headers=headers)
        site2 = BeautifulSoup(response.text, 'html.parser')
        marca = site2.find('a', class_='headerprodutosinfos__link btn-link-ka px-0').get('title')
        preco = produto.find('span', class_='blocoproduto__text blocoproduto__text--bold blocoproduto__price').get_text().strip()
        codigo = site2.find('p', class_='headerprodutosinfos__text ps-0 codigo-produto').get_text()
        codigo = codigo.replace("Código:","").strip()
        df.loc[j, 'Código'] = codigo
        df.loc[j,'Marca'] = marca
        df.loc[j,'Descrição'] = nome
        df.loc[j,'Preço'] = preco
        j += 1
        
i = 0
for linha in df['Preço']:
    valor = linha.replace('R','').replace('$','').replace('.','').replace(',','.').split()[0]
    df['Preço'][i] = valor
    i +=1

df['Preço'] = df['Preço'].astype(float)

df.to_excel('C:/Users/ma057659/Desktop/Matheus/Kalunga.xlsx', index=False)
print('\n \n')
print("RESUMO ESTATÍSTICO DOS PREÇOS\n\n")
print(df['Preço'].describe())

df.to_excel(salvar_excel+nome_arquivo+'.xlsx', index=False)
print("Operação concluída com sucesso! Visite o local do arquivo informado anteriormente.")




