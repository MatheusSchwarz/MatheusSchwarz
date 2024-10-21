# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 07:46:00 2023

@author: metma
"""

# https://dadosabertos.rfb.gov.br/CNPJ/

#Importando as bibliotecas que serão utilizadas
import requests
import zipfile
import shutil
import os
import pandas as pd
import sqlite3


#Definindo os locais em que os arquivos serão salvos
local_download = r'C:\Users\ma057659\Desktop\Matheus\Banco de dados CNAE\Download temporário'
local_db = r'C:\Users\ma057659\Desktop\Matheus\Banco de dados CNAE'
nome_db = 'db_cnae'


#URL para retirar as informações
url = 'https://dadosabertos.rfb.gov.br/CNPJ/'
#Tratando o arquivo informado anteriormente
nome_db = nome_db+'.db'

#loop for para montar o database de MEI
for i in range(0,1):
    i = str(i)
    arquivo = 'Simples'+'.zip'

    # Abrindo a página da internet e baixando o zip no computador
    r = requests.get(url+'/'+arquivo, allow_redirects=True)
    open(local_download+'/'+arquivo, 'wb').write(r.content)
    
    
    # Extraindo o arquivo .zip e renomeando para um nome conhecido
    nome_arquivo = zipfile.ZipFile(local_download+'/'+arquivo, 'r').namelist()[0]
    shutil.unpack_archive(local_download+'/'+arquivo, extract_dir = local_download)
    os.rename(local_download+'/'+nome_arquivo, local_download+'/'+arquivo[0:-3]+'csv')

    # Abrindo o arquivo baixado no pandas para testar                                                                                                                                                                                                                                                                
    df = pd.read_csv(local_download+'/'+arquivo[0:-3]+'csv', sep=';', encoding='latin1', header=None, dtype={0:'string',
                                                                                                                                          1:'string',
                                                                                                                                          2:'string',
                                                                                                                                          3:'string',
                                                                                                                                          4:'string',
                                                                                                                                          5:'string',
                                                                                                                                          6:'string'})
    
    df.columns = ['cnpj_basico', 'opcao_simples','data_opcao_simples','data_exclusao_simples','opcao_MEI','data_opcao_MEI','data_exclusao_MEI']
    
    # Criando o banco de dados através do sqlite3
    conn = sqlite3.connect(local_db+'/'+nome_db)
    c = conn.cursor()
    
    # Começando a criar as tabelas   
    c.execute('''
              CREATE TABLE IF NOT EXISTS Simples
              ([cnpj_basico] TEXT,
               [opcao_simples] TEXT,
               [data_opcao_simples] TEXT,
               [data_exclusao_simples] TEXT,
               [opcao_MEI] TEXT,
               [data_opcao_MEI] TEXT,
               [data_exclusao_MEI] TEXT)
              ''')
    
    df.to_sql('Simples', conn, if_exists='append', index=False)
    
    conn.commit()
    