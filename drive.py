# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:56:26 2019

@author: User
"""


import numpy as np
import socketio
import eventlet
from flask import Flask
from keras.models import load_model
import cv2
from io import BytesIO
from PIL import Image
import base64
 

sio=socketio.Server()   #Creates a wsgi server

app=Flask(__name__)#'__main__'    #Initialize an app
#A flask app


#Image preprocessing steps
speed_limit=10

def img_preprocess(img):     #To predict, we preprocess
    img=np.asarray(img)
    img=cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
    img=cv2.GaussianBlur(img,(3,3),0)
    img=cv2.resize(img,(200,66))
    img=img/255
    return img
    
@sio.on('telemetry')    #Give an automatic instruction and make connected

def telemetry(sid,data):   #con invokes telemetry 
    speed=float(data['speed'])
    image=Image.open(BytesIO(base64.b64decode(data['image'])))
    image=np.asarray(image)
    image=img_preprocess(image)
    image=np.array([image])
    steering_angle=float(model.predict(image))
    throttle=1.0-speed/speed_limit
    send_control(steering_angle,throttle)


@sio.on('con')   #Server object on, then connect 

def con(sid,environ):
    print('connected')
    send_control(0,0)    #Initialize values like speed = 0
    
def send_control(steering_angle,throttle):
    sio.emit('steer',data={'steering_angle':steering_angle.__str__(),'throttle':throttle.__str__()})


if __name__=="__main__":
    model=load_model('model.h5')
    app=socketio.Middleware(sio,app)
    eventlet.wsgi.server(eventlet.listen(("",4567)),app)   #Port no.


























































































































