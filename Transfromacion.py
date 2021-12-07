import math as m
import numpy as np

O1 = False
O2 = False
T = np.array([[0,0,0,17],[0,0,0,0],[0,0,0,49],[0,0,0,0]])
print("Mientras tanto, la Traslación será: \n",T)
contador = 0
Rx = np.array([[1,0,0,0],[0,-1,-(0),0],[0,0,-1,0],[0,0,0,1]])
Rz = np.array([[0,-(1),0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
R = np.dot(Rx,Rz)
Tf = T+R
print("Transformación final:\n",Tf)
while 1:

    print("Inserte un punto a transformar. (Cámara)")
    x = int(input("Coordenada X: ->"))
    y = int(input("Coordenada Y: ->"))
    z = int(input("Coordenada Z: ->"))
    punto = np.array([[x],[y],[z],[1]])
    puntoTransformado = np.dot(Tf,punto)

    print("Su punto inicial es: \n",punto,"\nY su punto transformado es: \n", puntoTransformado)
    print("---------------------------------------------------------------")