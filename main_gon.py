
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
import argparse

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

'''
def gen(camera):
    #get camera frame
    lower_green= np.array([8, 60, 0])
    upper_green = np.array([79, 101, 55])
    min_area = 4
    while True:
        frame = camera.get_frame()
        
        mask1 = cv2.inRange(frame, lower_green, upper_green)
        #frame = cv2.bitwise_and(frame, frame, mask=mask1)
        contours, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
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
'''



#AGPARSE para los argumentos del programa
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# Tener la imagen, pasarla a grey y clonar la original para el final
frame = camera.get_frame()
output = image.copy()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Ver si hay circulos
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    # show the output image
    cv2.imshow("output", np.hstack([frame, output]))
    cv2.waitKey(0)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
    