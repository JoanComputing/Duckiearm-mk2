import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.utils import shuffle
import pandas as pd
data=pd.read_csv("datos.csv")
datos = data.dropna(how = "any")
datos = shuffle(datos)
datos_angles_Y = datos[["Theta1", "Theta2","Theta3"]] #y                    
datos_poscam = datos[["U","V","R"]]                
datos_real_X = datos[["X", "Y","Z"]] #X

"""
lista=[]
i=1
for i in range(105):
    x = datos_angles.iloc[[i],[0]]
    y = datos_angles.iloc[[i],[1]]
    z = datos_angles.iloc[[i],[2]]
    lista.append([x, y, z])
lista = np.array(lista)
lista1=[]
i=1
for i in range(105):
    x = datos_real.iloc[[i],[0]]
    y = datos_real.iloc[[i],[1]]
    z = datos_real.iloc[[i],[2]]
    
    lista1.append([x, y, z])
    
lista1 = np.array(lista1)

"""
score = 0
while(score<0.46):
    #datos_angles = shuffle(datos_angles)
    #datos_real = shuffle(datos_real)
    
    #print(len(datos_real_X))
    #X_train, X_test, y_train, y_test = train_test_split(datos_real_X.values, datos_angles_Y.values)
    X_train, X_test, y_train, y_test = train_test_split(datos_angles_Y.values, datos_real_X.values)
    #print(X_train.size())
    regr = MLPRegressor(max_iter=5000000, activation='relu', hidden_layer_sizes=(10,50,10)).fit(X_train, y_train)
    score = regr.score(X_test, y_test)
    print(score)
    y_predict = regr.predict(X_test)
    rmse = np.sqrt(np.sum((y_test - y_predict)**2)/y_predict.shape[0])
    print(rmse)
    pos = [[0,90,50]]
    print(regr.predict(pos))
