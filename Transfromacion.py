import math as m
import numpy as np
import cv2
from camera import VideoCamera

T = np.array([[0,0,0,170],[0,0,0,0],[0,0,0,490],[0,0,0,0]])
#print("Mientras tanto, la Traslación será: \n",T)
#contador = 0
Rx = np.array([[1,0,0,0],[0,-1,-(0),0],[0,0,-1,0],[0,0,0,1]])
Rz = np.array([[0,-(1),0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
R = np.dot(Rx,Rz)
Tf = T+R
#print("Transformación final:\n",Tf)
"""
while 1:

    print("Inserte un punto a transformar. (Cámara)")
    x = float(input("Coordenada X: ->"))
    y = float(input("Coordenada Y: ->"))
    z = float(input("Coordenada Z: ->"))
    punto = np.array([[x],[y],[z],[1]])
    puntoTransformado = np.dot(Tf,punto)

    print("Su punto inicial es: \n",punto,"\nY su punto transformado es: \n", puntoTransformado)
    print("---------------------------------------------------------------")
    
"""
fx = 295.65
fy = 295.76
cx = 147.25
cy = 119.51

def z(r):
    #print(10*(fx/r))
    return 10*(fx/r)
    
def TransU(u,z):
    Px = ((u-cx)/fx)*z
    #print(Px)
    return Px
    
    
def TransV(v,z):
    Py = ((v-cy)/fy)*z
    #print(Py)
    return Py


def Transformada(Px,Py,Pz):

    punto = np.array([[Px],[Py],[Pz],[1]])
    #print(punto)
    puntoTransformado = np.dot(Tf,punto)
    #print(puntoTransformado)
    x = puntoTransformado[0]
    y = puntoTransformado[1]    
    z = puntoTransformado[2]
    #print(x,y,z)
    return float(x),float(y),float(z)
    
def TransFinal(u,v,r):
    Pz = z(r)
    Px = TransU(u,Pz)
    Py = TransV(v,Pz)
    x,y,zz = Transformada(Px,Py,Pz)
    return x,y,zz


def detectarCirculo(camera):
    x=None
    y=None
    r=None
    frame = camera.get_frame()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    circle=cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp=1,minDist=20,param1=60,param2=40,minRadius=5,maxRadius=24)
    if circle is not None:
      circle=np.round(circle[0,:])
      for x,y,r in circle:
        x=int(x)
        y=int(y)
        r=int(r)
            
        if r<16:
           #print (x,y,r)
           cv2.circle(frame,(x,y),r,(0,255,0),1)
           cv2.rectangle(frame,(x-5,y-5),(x+5,y+5),(0,128,255,-1))
              
           last_x = str(x)
           last_y = str(y)
           last_r = str(r)
              
           cv2.imwrite('prueba.png', frame)
    return x,y,r

#camera = VideoCamera(flip=False)
#u,v,r = detectarCirculo(camera)

#print(u,v,r)