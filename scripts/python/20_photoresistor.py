#!/usr/bin/env python
import eventlet
eventlet.monkey_patch()

import logging
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import json

DO = 17
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode='eventlet')

def setup():
  ADC.setup(0x48)
  GPIO.setup(DO, GPIO.IN)

# our gloabal worker
workerObject = None

class Worker(object):

    switch = False
    unit_of_work = 0

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = True

    def do_work(self):
        """
        do work and emit message
        """

        while self.switch:
            self.unit_of_work += 1

            print 'Value: ', ADC.read(0)
            self.socketio.emit('sensor_data', {'data': str(ADC.read(0))})

            # important to use eventlet's sleep method
            eventlet.sleep(0.5)

    def play(self):
        """
        resume the loop
        """
        self.switch = True

    def stop(self):
        """
        stop the loop
        """
        self.switch = False

@socketio.on('connect')
def connect():
    """
    connect
    """

    global worker
    worker = Worker(socketio)
    emit("re_connect", {"msg": "connected"})

@socketio.on('sensor_start')
def start_work():
    """
    trigger background thread
    """

    # notice that the method is not called - don't put braces after method name
    socketio.start_background_task(target=worker.play)
    socketio.start_background_task(target=worker.do_work)

@socketio.on('sensor_stop')
def stop_work():
    """
    trigger background thread
    """

    worker.stop()
    emit("update", {"msg": "worker has been stoppped"})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def main():
    print "Server listening at http://localhost:8888"
    setup()
    socketio.run(app, host='0.0.0.0', port=8888)

if __name__ == '__main__':
    main()
