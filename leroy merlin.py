# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:08:47 2023

@author: ma057659
"""

"""Importando as bibliotecas que irei utilizar"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

termo_procurado = str(input('\nO que você quer pesquisar na Leroy Merlin?\n'))

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

print("Operação em andamento, por favor, aguarde.")
driver = webdriver.Chrome()

"""Acessando a página e inserindo o termo a ser buscado na barra de pesquisa"""
driver.get('https://www.leroymerlin.com.br/')
time.sleep(2)
driver.find_element(By.CLASS_NAME, 'css-5ydu0l-button-button--stretch').click()
driver.find_element(By.ID, 'searchbar').click()
busca = driver.find_element(By.ID, 'searchbar')
busca.send_keys(termo_procurado)
busca.send_keys(Keys.RETURN)
time.sleep(2)


"""Descobrindo quantas páginas o programa irá rodar"""
try:
    testadorA = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[5]/button').text
except:
    try:
        testadorB = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[4]/button').text
    except:
        try:
            testadorB = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[3]/button').text
        except:
            try:
                testadorB = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[2]/button').text
            except:
                testadorB = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[2]/button').text

global j
j = 0

for produto in range(1,37):  
    try:
        preco = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[2]/a/div/div/span[1]').text
        df.loc[j,'Preço'] = preco
        link = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[1]/a').get_attribute('href')
        df.loc[j, 'Link'] = link
        driver.get(link)
        time.sleep(2)
        
        try:
            tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[4]/div[2]/table').text
        except:
            tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[3]/div[2]/table').text
        lista = tabela.split('\n')
        lista = pd.Series(lista)
        lista = lista[lista.str.contains('Marca')]
        marca = str(list(lista)).replace("Marca ","")
        marca = marca[2:-2]
        df.loc[j,'Marca'] = marca
        descricao = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[1]/h1').text
        df.loc[j, 'Descrição'] = descricao
        sku = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div').text
        sku = sku.replace("Cód.",'').strip()
        df.loc[j, 'SKU'] = sku
        j +=1
        driver.back()
        time.sleep(2)
    except:
        driver.back()
    
global contador
contador = 4

try:
    testadorA == testadorA
    while contador>0:
        try:
            try:
                driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/button[3]').click()
            except:
                driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/button[1]').click()
            time.sleep(3)
            if testadorA == driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[5]/button').text:
                contador -=1
            else:
                testadorA = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/div/div[5]/button').text
            for produto in range(1,37):   
                preco = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[2]/a/div/div/span[1]').text
                df.loc[j,'Preço'] = preco
                link = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[1]/a').get_attribute('href')
                df.loc[j, 'Link'] = link
                driver.get(link)
                time.sleep(2)
                try:
                    tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[4]/div[2]/table').text
                except:
                    tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[3]/div[2]/table').text
                lista = tabela.split('\n')
                lista = pd.Series(lista)
                lista = lista[lista.str.contains('Marca')]
                marca = str(list(lista)).replace("Marca ","")
                marca = marca[2:-2]
                df.loc[j,'Marca'] = marca
                descricao = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[1]/h1').text
                df.loc[j, 'Descrição'] = descricao
                sku = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div').text
                sku = sku.replace("Cód.",'').strip()
                df.loc[j, 'SKU'] = sku
                j +=1
                driver.back()
                time.sleep(2)
        except:
            j+=1
            driver.back()
except:
    testadorB == testadorB
    for pagina in range(1,int(testadorB)):
        try:
            try:
                driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/button[3]').click()
            except:
                driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[4]/nav/button[1]').click()
            time.sleep(2)
            for produto in range(1,37):   
                preco = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[2]/a/div/div/span[1]').text
                df.loc[j,'Preço'] = preco
                link = driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[1]/div[2]/div[3]/div/div/div['+str(produto)+']/div[1]/a').get_attribute('href')
                df.loc[j, 'Link'] = link
                driver.get(link)
                time.sleep(2)
                try:
                    tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[4]/div[2]/table').text
                except:
                    tabela = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[3]/div[2]/table').text
                lista = tabela.split('\n')
                lista = pd.Series(lista)
                lista = lista[lista.str.contains('Marca')]
                marca = str(list(lista)).replace("Marca ","")
                marca = marca[2:-2]
                df.loc[j,'Marca'] = marca
                descricao = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[1]/h1').text
                df.loc[j, 'Descrição'] = descricao
                sku = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div').text
                sku = sku.replace("Cód.",'').strip()
                df.loc[j, 'SKU'] = sku
                j +=1
                driver.back()
                time.sleep(2)
        except:
            j+=1
            driver.back()

df['Preço'] = df['Preço'].str.replace('R$',"").str.strip()

df.to_excel(salvar_excel+nome_arquivo+'.xlsx', index=False)
print("Operação concluída com sucesso. Por favor, verifique o arquivo no local informado.")