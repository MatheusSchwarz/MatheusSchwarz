# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 08:08:28 2024

@author: ma057659
"""
#Importando as funções que serão utilizadas
import pandas as pd
from datasets import Dataset, ClassLabel
from transformers import pipeline
from transformers import BartTokenizerFast
from transformers import BartForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
from torch import nn
from huggingface_hub import login

#Por que tive que fazer o Fine Tunning?
    #Verifiquei que o modelo original atribui sempre um peso negativo para a palavra "Nota"


login('#####') #Insira a sua chave aqui.

#Importando o dataset em que o modelo será treinado
org_df = pd.read_excel(r'C:\Users\ma057659\Desktop\Matheus\bart - facebook\astec junho.xlsx')
org_df.columns = ['text','class']

X = org_df['text']
y = org_df['class']

#Dividindo o dataset em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

df_train = pd.DataFrame({'text':X_train,'class':y_train})
df_test = pd.DataFrame({'text':X_test,'class':y_test})
le = LabelEncoder()
df_train['class'] = le.fit_transform(df_train['class'])
df_test['class'] = le.transform(df_test['class'])
classes = le.classes_

#Convertendo o dataframe para um Dataset objects
train_ds = Dataset.from_pandas(df_train, split='train')
test_ds = Dataset.from_pandas(df_test, split='test')
train_ds = train_ds.remove_columns('__index_level_0__')
test_ds = test_ds.remove_columns('__index_level_0__')

new_features = train_ds.features.copy()
new_features['class'] = ClassLabel(names=['negativo','positivo'])
train_ds = train_ds.cast(new_features)
test_ds = test_ds.cast(new_features)

features = train_ds.features
id2label = {idx:features['class'].int2str(idx) for idx in range(2)}
label2id = {v:k for k,v in id2label.items()}

#Importando o tokenizador do modelo bart
tokenizer = BartTokenizerFast.from_pretrained('facebook/bart-large-mnli')

#Usando o tokenizador para converter o texto
def tokenize_text(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512)

train_ds_tokenized = train_ds.map(tokenize_text, batched=True)
test_ds_tokenized = test_ds.map(tokenize_text, batched=True)


#Lidando com o desbalanceamento entre as classes
class_weights = 1 - df_train['class'].value_counts().sort_index() / len(df_train['class'])
class_weights = class_weights.to_numpy()
class_weights = torch.from_numpy(class_weights).float()

#renomeando a coluna 'class' para 'labels' para que o nn.CrossEntropyLoss identifique a coluna
train_ds_tokenized = train_ds_tokenized.rename_column('class','labels')
test_ds_tokenized = test_ds_tokenized.rename_column('class','labels')


class WeightedLossTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        #Feed inputs to model and extract logits
        outputs = model(**inputs)
        logits = outputs.get('logits')
        #Extract Labels
        labels = inputs.get('labels')
        #Define loss function with class weights
        loss_func = nn.CrossEntropyLoss(weight=class_weights)
        #Compute loss
        loss = loss_func(logits, labels)
        return (loss, outputs) if return_outputs else loss

#Importando o modelo
model = BartForSequenceClassification.from_pretrained('facebook/bart-large-mnli', num_labels=2, id2label=id2label, label2id=label2id, ignore_mismatched_sizes=True)

#definindo os argumentos para serem utilizados no treinamento do modelo
batch_size = 8
logging_steps = len(train_ds) // batch_size
output_dir = r'C:\Users\ma057659\Desktop\Matheus\bart - facebook\finetuned'
training_args = TrainingArguments(output_dir = output_dir,
                                  num_train_epochs=5,
                                  learning_rate = 2e-5,
                                  per_device_train_batch_size=batch_size,
                                  per_device_eval_batch_size=batch_size,
                                  weight_decay=0.01,
                                  evaluation_strategy='epoch',
                                  logging_steps=logging_steps,
                                  push_to_hub=True
                                  )

#Criando o objeto que irá treinar o modelo
trainer = WeightedLossTrainer(model=model,
                              args=training_args,
                              # compute_metrics=compute_metrics,
                              train_dataset=train_ds_tokenized,
                              eval_dataset=test_ds_tokenized,
                              tokenizer=tokenizer)

#treinando o modelo
trainer.train()

#salvando o modelo
trainer.save_model(r'C:\Users\ma057659\Desktop\Matheus\bart - facebook\zero-shot')

#Rodando o modelo
pipe = pipeline('zero-shot-classification', model=r'C:\Users\ma057659\Desktop\Matheus\bart - facebook\zero-shot')

sequencia = 'Nota 10.'
rotulos = ['negativo','positivo']
resultado = pipe(sequencia,rotulos)


