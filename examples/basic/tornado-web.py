#!/usr/bin/env python
# coding: utf-8

import os
import logging
import logging.config
import logging.handlers

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options


class MySysLogHandler(logging.handlers.SysLogHandler):

    def __init__(self, **kwargs):
        ident = kwargs.pop('ident', 'python')
        kwargs.setdefault('facility', 'local6')
        kwargs.setdefault('address', '/dev/log')
        super(MySysLogHandler, self).__init__(**kwargs)
        self.ident = ident

    def format(self, record):
        msg = super(MySysLogHandler, self).format(record)
        return u'{}[{}]: {}'.format(self.ident, record.process, msg)


log_config = {
    'version': 1,
    'formatters': {
        'local': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        }
    },
    'handlers': {
        'syslog': {
            'class': '{}.MySysLogHandler'.format(__name__),
            'formatter': 'local',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['syslog']
    },
}
logging.config.dictConfig(log_config)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info(u'get: Hello, world 你好')
        self.write("Hello, world")


def make_app():
    settings = {'debug': True}
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)


if __name__ == "__main__":
    define("port", type=int, default=8877, help="The port listen on")
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
