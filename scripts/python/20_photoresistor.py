#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from tornado import websocket, web, ioloop
import json

DO = 17
GPIO.setmode(GPIO.BCM)
cl = []
isPlaying = True

def setup():
  ADC.setup(0x48)
  GPIO.setup(DO, GPIO.IN)


def loop(ws):
  status = 1
  while isPlaying:
    print 'Value: ', ADC.read(0)
    ws.write_message(str(ADC.read(0)))
    time.sleep(0.2)

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
            loop(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
      if message == 'pause':
        isPlaying = False

      if message == 'play':
        isPlaying = True

app = web.Application([
    (r'/ws-photoresistor', SocketHandler),
])


if __name__ == '__main__':
  try:
    setup()
    app.listen(8888)
    ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass
