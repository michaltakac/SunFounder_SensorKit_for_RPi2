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

def setup():
  ADC.setup(0x48)
  GPIO.setup(DO, GPIO.IN)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/ws-photoresistor", SocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

class SocketHandler(websocket.WebSocketHandler):
  is_playing = True

  def open(self):
    self.stream.set_nodelay(True)
    print 'opening %s' % self
    if self not in cl:
      cl.append(self)
      while SocketHandler.is_playing:
        print 'Value: ', ADC.read(0)
        self.write_message(str(ADC.read(0)))
        time.sleep(0.2)

  def on_pong(self, data):
    print 'got pong', data

  def on_close(self):
    if self in cl:
        cl.remove(self)
        SocketHandler.is_playing = False

  def on_message(self, message):
    self.write_message(message)
    print message
    if message == 'pause':
      SocketHandler.is_playing = False
      print "is_playing? ", SocketHandler.is_playing

    if message == 'play':
      SocketHandler.is_playing = True
      print "is_playing? ", SocketHandler.is_playing


def main():
    setup()
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print "Server listening at http://localhost:", options.port
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
