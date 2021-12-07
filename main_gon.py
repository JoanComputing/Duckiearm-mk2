
#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages

import sys
sys.path.append('../')
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
import cv2
import numpy as np
import argparse

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here


def gen(camera):

    #Parámetros para la detección de color
     ##eSTOS PARAMETROS ESTAN RE CAMBIADOS PQ ESTABA PROBANDO, LOS ORIGINALES ESTAN EN MAIN.PY
    lower_green= np.array([0, 40, 0])  #RGB 0 40 0
    upper_green = np.array([79, 101, 55]) #RGB 79 101 55
    min_area = 40
    last_x = ''
    last_y = ''
    last_r = ''
    while True:
        #x,y,z = detectarCirculo(frame)
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
              
        cv2.putText (frame, (last_x+","+last_y+","+last_r), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255),1)
        '''
        #esta parte es para detectar por color
        
        mask1 = cv2.inRange(frame, lower_green, upper_green)
        #frame = cv2.inRange(frame, lower_green, upper_green)
        frame = cv2.bitwise_and(frame, frame, mask=mask1)
        
        contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # Obtener rectangulo que bordea un contorno
            AREA = cv2.contourArea(cnt)
            #Filtrar por area minima
            if AREA > min_area: # DEFINIR AREA
                x1,y1,w1,h1 = cv2.boundingRect(cnt)
                #Dibujar rectangulo en el frame original
                cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (255,0,0), 1)
                cv2.rectangle(frame, (0,0), (10,10), (0,255,0), -1)
                #print(x1+w1,y1+h1)
                #print(AREA)
                print("lado:",w1,h1)
                print( "cuadrado:",x1,y1)
               #print("centro del cuadrado:" ,xc,yc)
                cv2.putText (frame, ("Radio: "+str((w1/2)+2)), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255),2)
        '''

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
    
##
#se#