#!/usr/bin/env python

import bottle
import time
import threading
import sys


class ContentGenerator(object):

    def __init__(self, handler):
        self.running = True
        self.counter = 0
        self.handler = handler

    def __iter__(self):
        return self

    def next(self):
        if not self.running:
            print 'stopping {}/{}'.format(threading.current_thread(), self)
            raise StopIteration
        time.sleep(2)
        self.counter += 1
        data = 'event: progress\ndata: {{"progress": {}, "thread": "{}", "generator": "{}"}}\n\n'.format(self.counter, threading.current_thread(), self)
        print 'next {}/{}'.format(threading.current_thread(), self)
        return data

    def close(self):
        print 'close {}/{}'.format(threading.current_thread(), self)
        self.running = False


class Foo(object):

    def handle_eventsource(self):
        bottle.response.content_type = 'text/event-stream';
        print threading.current_thread()
        return ContentGenerator(self)

    def run(self, server_type='wsgiref'):
        app = bottle.Bottle()
        app.route('/', method=['GET'], callback=self.handle_eventsource)
        app.run(server=server_type)


foo = Foo()
foo.run(sys.argv[1])

