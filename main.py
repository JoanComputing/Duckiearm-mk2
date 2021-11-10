#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages

import sys
sys.path.append('../')
from flask import Flask, render_template, Response, request
from stream_server.camera import VideoCamera
import time
import threading
import os
import cv2
import numpy as np

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    lower_green= np.array([0, 0, 0])
    upper_green = np.array([0, 205, 100])
    min_area = 40
    while True:
        frame = camera.get_frame()
        
        mask1 = cv2.inRange(frame, lower_green, upper_green)
        #frame = cv2.bitwise_and(frame, frame, mask=mask1)
        contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            print(cnt)
            # Obtener rectangulo que bordea un contorno
            AREA = cv2.contourArea(cnt)
            #Filtrar por area minima
            if AREA > min_area: # DEFINIR AREA
                x,y,w,h = cv2.boundingRect(cnt)
                #Dibujar rectangulo en el frame original
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), -1)
                
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
    


