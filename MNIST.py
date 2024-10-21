# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:14:30 2024

@author: ma057659
"""

import tensorflow as tf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

# im = Image.open(r'C:\Users\ma057659\Desktop\Matheus\search.png')
# newsize = (24,24)
# im_resize = im.resize(newsize)
# im_resize.show()

#Fazendo o download dos datasets já tratados
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#Verificando se as classes estão equilibradas
sns.countplot(y_train)

#Verificando se há valores nulos
np.isnan(x_train).any()
np.isnan(x_test).any()

#Normalizando os valores
input_shape = (28,28,1)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2],1)
x_train = x_train / 255.0
x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2],1)
x_test = x_test/255.0

#Aplicando one-hot encoding nas tabelas y's

y_train = tf.one_hot(y_train.astype(np.int32),depth=10)
y_test = tf.one_hot(y_test.astype(np.int32),depth=10)

#Visualizando os dados
plt.imshow(x_train[100][:,:,0])
print(y_train[100])

#Criando o modelo CNN
batch_size = 64
num_classes = 10
epochs = 5

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (5,5), padding='same', activation='relu', input_shape=input_shape),
    tf.keras.layers.Conv2D(32, (5,5), padding='same', activation='relu'),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
    tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
    tf.keras.layers.MaxPool2D(strides=(2,2)),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.RMSprop(epsilon=1e-08), loss='categorical_crossentropy', metrics=['acc'])

#Treinando o modelo com os dados de treinamento
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('acc')>0.995):
      print("\nReached 99.5% accuracy so cancelling training!")
      self.model.stop_training = True

callbacks = myCallback()

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    validation_split=0.1,
                    callbacks=[callbacks])

#Prevendo os resultados do modelo
test_loss, test_acc = model.evaluate(x_test, y_test)


# Predict the values from the testing dataset
Y_pred = model.predict(x_test)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert testing observations to one hot vectors
Y_true = np.argmax(y_test,axis = 1)
# compute the confusion matrix
confusion_mtx = tf.math.confusion_matrix(Y_true, Y_pred_classes) 

#Matriz de confusão
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx, annot=True, fmt='g')

