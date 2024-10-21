# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:38:44 2024

@author: ma057659
"""

#Kaggle Titanic - Machine Learning from Disaster

#Importações
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler



#Importando os dados que serão utilizados no modelo
df = pd.read_csv(r'C:\Users\ma057659\Desktop\Matheus\Kaggle\Titanic\Dados\train.csv')
final = pd.read_csv(r'C:\Users\ma057659\Desktop\Matheus\Kaggle\Titanic\Dados\test.csv')

#Tratamento dos dados
df1 = df
df1['Survived'] = df1['Survived'].astype(int)

#Fazendo a exploração dos dados

df.info()
df.describe()
df.isnull().sum()
df['Embarked'].value_counts()

# sns.countplot(x='Survived', data=df)
# sns.boxplot(data=df,x='Survived',y='Age')
# sns.countplot(data=df1,x='Embarked', hue='Survived')
# sns.countplot(data=df1,x='Sex', hue='Survived')

    #Optei por fazer o drop das linhas sem informação em "Embarked", porque aparentemente essa coluna impacta para a predição e eu tenho todas as informações no arquivo de teste. Essa não é a etapa correta para fazer o tratamento dos dados, mas essa alteração não irá fazer com que haja vazamento de dados do treino para o teste
df.dropna(subset=['Embarked'], inplace=True)

#Dividindo os dados em X e y:
X = df[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']]
y = df['Survived']

#Divisão dos dados em treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X,y, test_size=0.25, random_state=42)

#Tratando os dados
le_sex = LabelEncoder()
X_treino['Sex'] = le_sex.fit_transform(X_treino['Sex'])
le_sex_labels = le_sex.classes_
X_teste['Sex'] = le_sex.transform(X_teste['Sex'])

se_mean = SimpleImputer(missing_values=pd.NA,strategy='mean')
se_mean.fit(X_treino[['Age']], y=None)
X_treino['Age'] = se_mean.transform(X_treino[['Age']])
X_teste['Age'] = se_mean.transform(X_teste[['Age']])

le_embarked = LabelEncoder()
X_treino['Embarked'] = le_embarked.fit_transform(X_treino['Embarked'])
le_embarked_labels = le_embarked.classes_
X_teste['Embarked'] = le_embarked.transform(X_teste['Embarked'])

scaler = StandardScaler().fit(X_treino)
X_train = scaler.transform(X_treino)
X_valid = scaler.transform(X_teste)


#Criando o modelo utilizando RandomForest
classifier = RandomForestClassifier(
     criterion='gini',
     max_depth=None,
)

classifier.fit(X_treino, y_treino)
score_treino = classifier.score(X_treino, y_treino)
score_teste = classifier.score(X_teste, y_teste)
print(f'Accuracy (Train): {score_treino:.4f}')
print(f'Accuracy (Teste): {score_teste:.4f}')
predicao = classifier.predict(X_teste)


#Prevendo os dados solicitados
X_pred = final[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']]

X_pred['Sex'] = le_sex.transform(X_pred['Sex'])
X_pred['Age'] = se_mean.transform(X_pred[['Age']])
X_pred['Embarked'] = le_embarked.transform(X_pred['Embarked'])
X_pred = scaler.transform(X_pred)

se_mean_fare = SimpleImputer(missing_values=pd.NA,strategy='mean')
X_pred['Fare'] = se_mean_fare.fit_transform(X_pred[['Fare']], y=None)


predicao = classifier.predict(X_pred)

resultado = final['PassengerId']
resultado = resultado.to_frame()
resultado['Survived_predict'] = predicao

resultado['PassengerId'] = resultado['PassengerId'].astype(str)
resultado['Survived_predict'] = resultado['Survived_predict'].astype(str)
resultado.rename(columns={'Survived_predict':'Survived'}, inplace=True)

resultado.to_csv(r'C:\Users\ma057659\Desktop\Matheus\Kaggle\Titanic\previsao.csv', sep=',', index=False)
