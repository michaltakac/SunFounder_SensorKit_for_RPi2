#!/usr/bin/env python
import logging
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from tornado import websocket, web, ioloop
import tornado.options
import json

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/ws-photoresistor", SocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

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
      logging.info("got message %r", message)
      if message == 'pause':
        isPlaying = False

      if message == 'play':
        isPlaying = True


def main():
    setup()
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
