# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 12:03:59 2023

@author: metma
"""

#Importando as bibliotecas que serão utilizadas
import requests
import zipfile
import shutil
import os
import pandas as pd
import sqlite3
import time

#Definindo os locais em que os arquivos serão salvos
local_download = r'C:\Users\ma057659\Desktop\Matheus\Banco de dados CNAE\Download temporário'
local_db = r'C:\Users\ma057659\Desktop\Matheus\Banco de dados CNAE'
nome_db = 'db_cnae'

#URL para retirar as informações
url = 'https://dadosabertos.rfb.gov.br/CNPJ/'
#Tratando o arquivo informado anteriormente
nome_db = nome_db+'.db'


# Abrindo a conexão com o banco de dados
conn = sqlite3.connect(local_db+'/'+nome_db)
c = conn.cursor()


#Criando uma coluna na tabela Estabelecimentos que vai receber o cnpj completo do estabelecimento
c.execute('''
          ALTER TABLE Estabelecimentos
          ADD cnpj TEXT
          ''')
c.execute('''
          UPDATE Estabelecimentos
          SET cnpj = Estabelecimentos.cnpj_basico || cnpj_ordem || cnpj_dv
          ''')

conn.commit()

#Criando índices para agilizar a consulta entre diferentes tabelas

c.execute('''
          CREATE INDEX indice_cnpj_basico ON Empresas(cnpj_basico)
          ''')

c.execute('''
          CREATE INDEX indice_cnpj_basico_estabelecimentos ON Estabelecimentos(cnpj_basico)
          ''')
          
c.execute('''
          CREATE INDEX indice_cnpj_simples ON Simples(cnpj_basico)
          ''')

conn.commit()

#Criando uma nova classificação para o porte da empresa considerando MEI

c.execute('''
          ALTER TABLE Empresas
          ADD porte2 TEXT
          ''')
 

c.execute('''
          UPDATE Empresas
          SET porte2 = (SELECT Simples.opcao_MEI
                        FROM Simples
                        WHERE Empresas.cnpj_basico = Simples.cnpj_basico
                        )
          ''')

conn.commit()

c.execute('''
          UPDATE Empresas
          SET cod_porte = CASE
          WHEN porte2 = 'S' THEN '02'
          WHEN cod_porte = '00' THEN '00'
          WHEN cod_porte = '03' THEN '03'
          WHEN cod_porte = '05' THEN '05'
          WHEN cod_porte = '01' THEN '01'
          END
          ''')

conn.commit()

c.execute('''
          ALTER TABLE Empresas DROP COLUMN porte2
          ''')
conn.commit()

#Criando novas colunas na tabela de Estabelecimentos

c.execute('''
          ALTER TABLE Estabelecimentos
          ADD cod_porte TEXT
          ''')
 

c.execute('''
          UPDATE Estabelecimentos
          SET cod_porte = (SELECT Empresas.cod_porte
                        FROM Empresas
                        WHERE Empresas.cnpj_basico = Estabelecimentos.cnpj_basico
                        )
          ''')

conn.commit()

c.execute('''
          ALTER TABLE Estabelecimentos
          ADD cod_uf INTEGER
          ''')
          
c.execute('''
          UPDATE Estabelecimentos
          SET cod_uf = CASE
          WHEN uf = 'AC' THEN 12
          WHEN uf = 'AL' THEN 27
          WHEN uf = 'AM' THEN 13
          WHEN uf = 'AP' THEN 16
          WHEN uf = 'BA' THEN 29
          WHEN uf = 'CE' THEN 23
          WHEN uf = 'DF' THEN 53
          WHEN uf = 'ES' THEN 32
          WHEN uf = 'GO' THEN 52
          WHEN uf = 'MA' THEN 21
          WHEN uf = 'MG' THEN 31
          WHEN uf = 'MS' THEN 50
          WHEN uf = 'MT' THEN 51
          WHEN uf = 'PA' THEN 15
          WHEN uf = 'PB' THEN 25
          WHEN uf = 'PE' THEN 26
          WHEN uf = 'PI' THEN 22
          WHEN uf = 'PR' THEN 41
          WHEN uf = 'RJ' THEN 33
          WHEN uf = 'RN' THEN 24
          WHEN uf = 'RO' THEN 11
          WHEN uf = 'RR' THEN 14
          WHEN uf = 'RS' THEN 43
          WHEN uf = 'SC' THEN 42
          WHEN uf = 'SE' THEN 28
          WHEN uf = 'SP' THEN 35
          WHEN uf = 'TO' THEN 17
          WHEN uf = 'EX' THEN 10
          END
          
          ''')

conn.commit()
