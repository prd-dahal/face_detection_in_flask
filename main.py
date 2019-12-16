#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import sys
import numpy

app = Flask(__name__)
faces_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    app.logger.info('Hello ')
    return render_template('index.html')

def get_frame():
    camera_port=0
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    while True:
        ret, image = camera.read()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faces_cascade.detectMultiScale(gray_image, 1.3, 5)
        img = image
        
        for x,y,w,h in faces:
            
            img = cv2.rectangle(image, (x,y),(x+w,y+h),(255,0,0),2)
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    del(camera)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
