# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:21:37 2022

@author: ma057659
"""

#Comandos úteis para lidar com dataframe
""" comandos para analisar a importação dos dados"""
#type(df) - retorna o tipo do objeto
# df.shape - retorna o número de linhas e colunas numa tupla
#df.info( ) - retorna o número total de linhas, nomes das colunas, número de dados não missing por coluna, tipo da coluna
#df.head() - retorna as 5 primeiras linhas do df
#df.tail() - retorna as 5 últimas linhas do df
#df.columns - retorna uma lista de nomes das colunas
#df.index - retorna um range com os números das linhas
#df.values - retorna a lista de valores do df
#df.dtypes - retorna o nome da coluna e o tipo dela
"""comandos para manipulação básica"""
#country = df["country"] - retorna somente a coluna country do df, como uma series
#country = df[["country]] - retorna somente a coluna country do df, como um df
#df.drop(["continent", "country"], axis="colums") - apaga as colunas continent e country do df. Necessita o argumento axis para especificar que está largando uma coluna.
#df.loc[0] - retorna a primeira linha como resultado
#df.loc[[0,1]] - retorna a primeira e a segunda linha como resultado, procurando pelo index
#df.iloc[[0,1,-1]] - retorna a primeira, segunda e última linha do df
#df.loc[:,["year","pop"]] - retorna todas as linhas da coluna year e pop
#df.loc[df["country"] == "United States", :] - Filtra a base por tudo que é United States
#df.loc[(df["country"] == "United States") & (df["year"] == 1982), :] - Filtra por country e year, necessita de parenteses para funcionar
#df.groupby(["year"]) - Agrupa todos os dados por ano, baseado na coluna chamada ano
#df.groupby(["year"]) ["lifeexp"].mean() - após agrupar as linhas por ano, retorna a lifeexp em forma de média
#df.groupby(["year"]) ["lifeexp"].agg(np.std) - a função agg (agregar) permite retornar qualquer valor utilizando um pacote diferente
#df.groupby(["year", "continent"]) [["lifeexp", "gdbpercap"]].agg(np.mean) - Retorna uma tabela de anos distintos, e dentro de cada ano os continentes. Calcula a média da lifeexp e do gdppercap.
#df.groupby(["year", "continent"]) [["lifeexp", "gdbpercap"]].agg(np.mean).reset_index() - traz de volta os índices de 0 a n da tabela gerada.
#df.melt(id_vars="religion")  - Transfere as colunas para linhas do df, id_vars informa a coluna que não se quer mexer
#df.melt(id_vars="religion", var_name="income", value_name="count") - define os nomes das colunas criadas após a agregação
# se você colocar parenteses no ínicio e no fim de uma expressão, você pode quebrar linhas a vontade que o python irá considerar como uma única expressão
#"hello_world".split("_") - divide a tring em uma lista com duas palavras
#df["cd_country"].str.split("_", expand=true) - divide a coluna cd_country em palavras, onde o separador é o _. O expand=True faz retornar um dataframe ao invés de uma lista
#df.pivot_table(index=["id","year","month","day"], columns = "element", values= "temp").reset_index() - pega os valores distintos da coluna element e os transforma em nova coluna.
"""coisas aletaórias úteis"""
# o underline não conta como parte de um número inteiro, por exemplo, 10_000_000 é lido como 10000000.
#a lista pode acabar com uma vírgula, que o python desconsidera ela no final
"""criar funções no Python"""
#def my_function(x,y)
    #pass - obrigatório o pass caso não queira escrever nada
    #return x**2+y
#assert 4*4 == 16 - se for verdadeiro nada acontece, se for falso, o assert irá retornar um erro
#df["a"].apply(my_exp, e=4) - tomando a coluna a do df, pega cada linha de a e eleva ao valor de e.

