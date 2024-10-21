# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:18:03 2023

@author: ma057659
"""

"""Importando as bibliotecas que irei utilizar"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

termo_procurado = str(input('\nO que você quer pesquisar no Mercado Livre?\n'))

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

"""extração automatizada Mercado Livre"""
palavra_chave = termo_procurado
palavra_chave = palavra_chave.replace(' ','-')
#Link em que a busca será realizada
link_site = 'https://lista.mercadolivre.com.br/'+palavra_chave
#Definindo o objeto 'driver' como um navegador do Google Chrome
driver = webdriver.Chrome()
#Abrindo o link no navegador
driver.get(link_site)
#Faz o código aguardar por 2 segundos antes de continuar, para garantir que toda a página será carregada antes de prosseguir
time.sleep(2)
#Descobrindo quantas páginas existem na busca
try:
    paginas = int(driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/section/div[9]/ul/li[2]').text.replace('de ',''))
except:
    paginas = int(driver.find_element(By.XPATH, '//*[@id="root-app"]/div/div[2]/aside/div[2]/span').text.replace(' resultados',''))

while True:
    try:
        busca = int(input('Essa pesquisa possui '+str(paginas)+' páginas, de quantas você deseja retirar informação?'))
        break
    except:
        print('Por favor, digite um número válido!')

print('Operação em andamento. Por favor, aguarde.')

global j
j = 0
global k
k = 0
global l
l = 0
pagina_do_mercado_livre = 0
for pagina_do_mercado_livre in range(0, busca):
    numeracao = str(pagina_do_mercado_livre*48+1)
    link_site = 'https://lista.mercadolivre.com.br/'+palavra_chave+'_Desde_'+numeracao
    driver.get(link_site)
    time.sleep(3)
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    try:
        produtos = site.find_all('div', class_='ui-search-result__wrapper shops__result-wrapper')        
    except:
        produtos = site.find_all('div', class_='ui-search-result__content')    
    for produto in produtos:
        descricao = produto.find('a', class_='ui-search-item__group__element shops__items-group-details ui-search-link').get_text()
        link = produto.find('a', class_='ui-search-item__group__element shops__items-group-details ui-search-link').get('href')
        preco = produto.find('span', class_='price-tag-fraction').get_text()
        try:
            centavos = produto.find('span', class_='price-tag-cents').get_text()
        except:
            centavos = str(00)
        valor = preco + ',' + centavos
        df.loc[j, 'Descrição'] = descricao
        df.loc[j, 'Link'] = link
        df.loc[j, 'Preço'] = valor
        j +=1
    
    #Acessando a página de cada produto para extrair o código do produto
    
    for link in df['Link'][k:]:
        driver.get(link)
        time.sleep(3)
    
        try:
            codigo = driver.find_element(By.XPATH, '//*[@id="technical_specifications"]/div/div[1]/table/tbody/tr[2]/td/span').text
            df.loc[k,'SKU'] = codigo
            k+=1
        except:
            df.loc[k,'SKU'] = 'Código não informado'
            k+=1
            
        try:
            marca = driver.find_element(By.XPATH, '//*[@id="technical_specifications"]/div/div[1]/table/tbody/tr[1]/td/span').text            
            df.loc[l,'Marca'] = marca
            l+=1
        except:
           df.loc[l,'Marca'] = 'Marca não informada'
           l+=1

df.to_excel(salvar_excel+nome_arquivo+'.xlsx', index=False)

print('Operação concluída. O arquivo encontra-se no local informado anteriormente.')

