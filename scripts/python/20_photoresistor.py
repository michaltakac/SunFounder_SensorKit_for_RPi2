#!/usr/bin/env python
import logging
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import json

DO = 17
GPIO.setmode(GPIO.BCM)
is_playing = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def setup():
  ADC.setup(0x48)
  GPIO.setup(DO, GPIO.IN)

def loop():
    while True:
        @socketio.on('sensor_stop')
        def handle_stop_event():
            print('Sensor stopped')
            break

        print 'Value: ', ADC.read(0)
        emit('sensor_data', {'data': str(ADC.read(0))})
        time.sleep(0.2)


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('sensor_start')
def handle_start_event():
    print('Sensor started')
    loop()


def main():
    print "Server listening at http://localhost:8888"
    setup()
    socketio.run(app, host='0.0.0.0', port=8888)

if __name__ == '__main__':
    main()
