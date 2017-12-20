#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
import logging

import redis
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
from tornado.options import define, options

from simple_syslog_handler import SimpleSysLogHandler


SimpleSysLogHandler.config_logging()
redis_key = datetime.now().strftime('tornado:%Y-%m-%d_%H:%M:%S')
redis_cli = redis.StrictRedis()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        redis_cli.incr(redis_key)
        logging.info(u'get: Hello, world 你好')
        self.write("Hello, world")


def make_app():
    settings = {
        'debug': True,
        # NOTE: https://stackoverflow.com/a/32527393/1274372
        #   `autoreload` is incompatible with multi-process mode.
        #   When autoreload is enabled you must run only one process.
        'autoreload': False,
    }
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)


if __name__ == "__main__":
    define("port", type=int, default=8877, help="The port listen on")
    define("processes", type=int, default=2, help="How many processes can run")
    tornado.options.parse_command_line()
    sys.stderr.write('Args(port={}, processes={}, redis-key={})\n'.format(
        options.port,
        options.processes,
        redis_key,
    ))

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    server.start(options.processes)
    tornado.ioloop.IOLoop.current().start()
