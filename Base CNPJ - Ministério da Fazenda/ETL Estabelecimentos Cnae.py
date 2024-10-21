# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 18:55:33 2023

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
url = 'https://dadosabertos.rfb.gov.br/CNPJ/dados_abertos_cnpj/2024-08/'
#Tratando o arquivo informado anteriormente
nome_db = nome_db+'.db'

#loop for para montar o database de Estabelecimentos
for i in range(0,10):
    i = str(i)
    arquivo = 'Estabelecimentos'+i+'.zip'

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
                                                                                                                                          6:'string',
                                                                                                                                          7:'string',
                                                                                                                                          8:'string',
                                                                                                                                          9:'string',
                                                                                                                                          10:'string',
                                                                                                                                          11:'string',
                                                                                                                                          12:'string',
                                                                                                                                          13:'string',
                                                                                                                                          14:'string',
                                                                                                                                          15:'string',
                                                                                                                                          16:'string',
                                                                                                                                          17:'string',
                                                                                                                                          18:'string',
                                                                                                                                          19:'string',
                                                                                                                                          20:'string',
                                                                                                                                          21:'string',
                                                                                                                                          22:'string',
                                                                                                                                          23:'string',
                                                                                                                                          24:'string',
                                                                                                                                          25:'string',
                                                                                                                                          26:'string',
                                                                                                                                          27:'string',
                                                                                                                                          28:'string',
                                                                                                                                          29:'string'} )
    
    df.columns = ['cnpj_basico', 'cnpj_ordem', 'cnpj_dv', 'cod_matriz_ou_filial', 'nome_fantasia', 'cod_situacao_cadastral', 'data_situacao_cadastral', 'cod_motivo_situacao_cadastral', 'nome_da_cidade_exterior',
                  'cod_pais', 'data_inicio_atividade', 'cnae_principal', 'cnae_secundario', 'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'uf', 'municipio', 'ddd1',
                  'telefone1', 'ddd2', 'telefone2', 'ddd_fax', 'fax', 'email', 'cod_situacao_especial', 'data_situacao_especial']
    
    # Criando o banco de dados através do sqlite3
    conn = sqlite3.connect(local_db+'/'+nome_db)
    c = conn.cursor()
    
    # Começando a criar as tabelas   
    c.execute('''
              CREATE TABLE IF NOT EXISTS Estabelecimentos
              ([cnpj_basico] TEXT,
               [cnpj_ordem] TEXT,
               [cnpj_dv] TEXT,
               [cod_matriz_ou_filial] TEXT,
               [nome_fantasia] TEXT,
               [cod_situacao_cadastral] TEXT,
               [data_situacao_cadastral] TEXT,
               [cod_motivo_situacao_cadastral] TEXT,
               [nome_da_cidade_exterior] TEXT,
               [cod_pais] TEXT,
               [data_inicio_atividade] TEXT,
               [cnae_principal] TEXT,
               [cnae_secundario] TEXT,
               [tipo_logradouro] TEXT,
               [logradouro] TEXT,
               [numero] TEXT,
               [complemento] TEXT,
               [bairro] TEXT,
               [cep] TEXT,
               [uf] TEXT,
               [municipio] TEXT,
               [ddd1] TEXT,
               [telefone1] TEXT,
               [ddd2] TEXT,
               [telefone2] TEXT,
               [ddd_fax] TEXT,
               [fax] TEXT,
               [email] TEXT,
               [cod_situacao_especial],
               [data_situacao_especial])
              ''')
    
    df.to_sql('Estabelecimentos', conn, if_exists='append', index=False)
    
    conn.commit()
