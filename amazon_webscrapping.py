# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:12:14 2023

@author: metma
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import pandas as pd
from math import ceil

global j
j=0
global n
n = 0

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
df = pd.DataFrame({"Marca":[],"Descrição":[],"Preço":[],"Avaliação":[], 'Patrocinado':[]})
termo_procurado = str(input('\nO que você quer pesquisar na Amazon?\n'))
while True:    
    try:
        salvar_excel = str(input('Insira o endereço onde você deseja salvar o arquivo: '))+ '\\'
        salvar_excel = salvar_excel.replace('\\','/')
        nome_arquivo = str(input('insira o nome do arquivo que deseja salvar: '))
        df.to_excel(salvar_excel+nome_arquivo+'.xlsx')
        break
    except:
        print('Por favor, insira um endereço e/ou nome de arquivo válido')
    
driver.get('https://www.amazon.com.br/')
driver.find_element(By.NAME, 'field-keywords').click()
busca = driver.find_element(By.NAME, 'field-keywords')
busca.send_keys(termo_procurado)
busca.send_keys(Keys.RETURN)
time.sleep(2)
numero_de_produtos = driver.find_element(By.XPATH, '//*[@id="search"]/span/div/h1/div/div[1]/div/div/span[1]').text
numero_de_produtos = numero_de_produtos.replace('1-48 de ','').replace(".","")
numero_de_produtos = re.findall(r'\d+',numero_de_produtos)
numero_de_produtos = int(numero_de_produtos[0])

numero_de_paginas = ceil(numero_de_produtos/48)
funcao = lambda x: numero_de_paginas if numero_de_paginas < 7 else 7
numero_de_paginas = funcao(numero_de_paginas)
get_url = driver.current_url
caracteres_termo_procurado = len(termo_procurado)
url = get_url[0:31+caracteres_termo_procurado] + 'page=' + '1' + '&' + get_url[31+caracteres_termo_procurado:]

print('Para essa busca a Amazon possui ',numero_de_paginas," paginas. De quantas você quer retirar informação? Obs: cada página demora em média 3 minutos para ser executada")

while True:
    try:
        decisao = int(input('\nDigite o número de páginas que deseja:\n'))
        break
    except:
        print('Por favor, digite um número válido!')  

print('Operação em andamento, por favor, aguarde.')
for iteracao in range(1, decisao+1):
    url = get_url[0:31+caracteres_termo_procurado] + 'page=' + str(iteracao) + '&' + get_url[31+caracteres_termo_procurado:]
    driver.get(url)
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')

    produtos = site.find_all('div', class_='a-section a-spacing-base')
    
    for produto in produtos:
        nome = produto.find('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-4').get_text()
        df.loc[j,"Descrição"] = nome
    
        try:
            nota = produto.find('span', class_='a-size-base').get_text()
            df.loc[j, 'Avaliação'] = nota
    
        except:
           df.loc[j, 'Avaliação'] = "Sem nota no site"
    
        try:
            valor = produto.find('span', 'a-price-whole').get_text()
            df.loc[j,'Preço'] = valor
            
        except:
            df.loc[j,'Preço'] = 'Produto sem preço'
            
        try:
            patrocinado = produto.find('span', class_='a-color-base').get_text()
            if patrocinado == "Patrocinado":    
                df.loc[j, 'Patrocinado'] = 'Produto Patrocinado'
            else:
                df.loc[j, 'Patrocinado'] = 'Não Patrocinado'  
        except:
            pass
        
        try:
             valor = produto.find('span', 'a-price-fraction').get_text()
             df.loc[j, 'Centavos'] = valor
             j +=1
        except:
            j +=1
            
       
    for link in produtos:
        try:
            endereco = link.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
            endereco_completo = 'https://www.amazon.com.br/' + endereco
            driver2.get(endereco_completo)
            time.sleep(1)
            tabela_info_produto = driver2.find_element(By.ID, 'productDetails_techSpec_section_1').text
            lista = tabela_info_produto.split('\n')
            lista = pd.Series(lista)
            lista = lista[lista.str.contains('Marca')]
            marca = str(list(lista)).replace("Marca ","")
            marca = marca[2:-2]
            df.loc[n,'Marca'] = marca
            df.loc[n, 'Link'] = endereco_completo
            n +=1
        except:
            try:
                endereco = link.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
                endereco_completo = 'https://www.amazon.com.br/' + endereco
                driver2.get(endereco_completo)
                time.sleep(1)
                tabela_info_produto = driver2.find_element(By.ID, 'productOverview_feature_div').text
                lista = tabela_info_produto.split('\n')
                lista = pd.Series(lista)
                lista = lista[lista.str.contains('Marca')]
                marca = str(list(lista)).replace("Marca ","")
                marca = marca[2:-2]
                df.loc[n,'Marca'] = marca
                df.loc[n, 'Link'] = endereco_completo
                n +=1
            except:
                endereco = link.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
                endereco_completo = 'https://www.amazon.com.br/' + endereco
                driver2.get(endereco_completo)
                df.loc[n, 'Link'] = endereco_completo
                df.loc[n, 'Marca'] = 'INSIRA A MARCA MANUALMENTE'
                n +=1

df['Preço'] = df['Preço'] + df['Centavos']
df = df.drop(columns='Centavos')


iterador = 0
for linha in df['Avaliação']:
    if 'em até' in linha or 'Mais opções' in linha or 'Economize' in linha:
        df.loc[iterador,'Avaliação'] = 'Sem nota no site'
        iterador +=1
    else:
        iterador +=1
   
contador = 0
for linha in df['Avaliação']:
    df.loc[contador,'Avaliação'] = df.loc[contador,'Avaliação'].replace('.',',')
    contador +=1    

df['Avaliação'] = [x if "R$" not in x else 'Sem nota no site' for x in df['Avaliação']]
df['Avaliação'] = df['Avaliação'].str.replace(",","")

df.to_excel(salvar_excel+nome_arquivo+'.xlsx', index=False)
print('Operação concluída com sucesso! O arquivo se encontra no local informado.')