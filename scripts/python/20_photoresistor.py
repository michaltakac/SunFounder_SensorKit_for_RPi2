#!/usr/bin/env python
import logging
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import json

define("port", default=8888, help="run on the given port", type=int)

DO = 17
GPIO.setmode(GPIO.BCM)
cl = []
is_playing = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def setup():
  ADC.setup(0x48)
  GPIO.setup(DO, GPIO.IN)

def loop():
    while is_playing:
        print 'Value: ', ADC.read(0)
        emit('sensor_data', {'data': str(ADC.read(0))})
        time.sleep(0.2)

class SocketHandler(websocket.WebSocketHandler):
  is_playing = True

  def check_origin(self, origin):
    return True

  def open(self):
    if self not in cl:
      cl.append(self)
      while SocketHandler.is_playing:
        print 'Value: ', ADC.read(0)
        self.write_message(str(ADC.read(0)))
        time.sleep(0.2)

  def on_close(self):
    if self in cl:
        cl.remove(self)
        SocketHandler.is_playing = False


@socketio.on('sensor_start')
def handle_start_event():
    is_playing = True

@socketio.on('sensor_stop')
def handle_stop_event():
    is_playing = False

def main():
    setup()
    loop()
    socketio.run(app)
    print "Server listening at http://localhost:", options.port

if __name__ == '__main__':
    main()
