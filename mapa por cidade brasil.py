# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:24:56 2022

@author: ma057659
"""

import plotly.io as pio

import pandas as pd
import json
import plotly.express as px

#with urlopen("https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=maxima&intrarregiao=UF") as response:
#    geojson = json.load(response, encoding='ISO-8859–1')


"""Importando o desenho do mapa para dentro do python"""
geojson = json.load(open("C:/Users/ma057659/Desktop/Matheus/brasil_completo.json", encoding='utf-8'))

"""Importando os dados a serem plotados"""    
dados = pd.read_excel("C:/Users/ma057659/Desktop/Trabalho/FERNANDA/Potencial varejo/teste.xlsx")

"""aplicando filtro nos dados para plotar uma parte específica do mapa"""
filtro = dados["UF"] == "SC"
dados = dados[filtro]


"""criando o mapa"""
fig = px.choropleth(dados,
                    geojson = geojson,
                    locations="Código IBGE",
                    featureidkey="properties.id",
                    color="Indicador",
                    hover_data=["Código IBGE"],
                    hover_name="Cidade",
                    color_continuous_scale=[[0, 'rgb(240,240,240)'],
                      [0.05, 'rgb(13,136,198)'],
                      [0.1, 'rgb(191,247,202)'],
                      [0.20, 'rgb(4,145,32)'],
                      [1, 'rgb(227,26,28,0.5)']],
                    labels="Cidade")

"""Dizendo para o Python mostrar somente a região de interesse no mapa"""
fig.update_geos(fitbounds="locations", visible=False)

"""dizendo para o python abrir o mapa numa aba do navegador quando terminar"""
pio.renderers.default='browser'

"""dizendo para mostrar o mapa"""
fig.show()
fig.write_html("C:/Users/ma057659/Desktop/Matheus/teste.html")