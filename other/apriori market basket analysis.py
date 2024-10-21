# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:26:41 2024

@author: ma057659
"""

#from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth
import pandas as pd

df = pd.read_excel(r'C:\Users\ma057659\Desktop\Trabalho\Python\apriori.xlsx')

df1 = pd.pivot_table(data=df, values='Qtd. SellOut', index='Revenda', columns='Item')

for coluna in df1:
    df1[coluna] = df1[coluna].apply(lambda x: 1 if x>0 else 0)


df1 = df1.astype('bool')
#suportes = apriori(df1, min_support=0.001, use_colnames=True)
suportes = fpgrowth(df1, min_support=0.001, use_colnames=True)

resultado = association_rules(suportes, metric='confidence', min_threshold=0.01)
resultado['len_antecedents'] = resultado['antecedents'].apply(lambda x: len(x))
resultado['len_consequents'] = resultado['consequents'].apply(lambda x: len(x))

resultado['antecedents'] = resultado['antecedents'].astype(str)
resultado['consequents'] = resultado['consequents'].astype(str)


resultado_desejado = resultado[(resultado['len_antecedents'] == 1) & (resultado['len_consequents'] == 1)]

resultado_desejado = resultado_desejado[resultado_desejado['consequents'].apply(lambda x: True if 'FONTES' in x else False)]

resultado.to_excel(r'C:\Users\ma057659\Desktop\Trabalho\Greyce\Compartilhamento com a equipe\3 - Market Basket Analysis\exemplo\exemplo.xlsx', index=False)
