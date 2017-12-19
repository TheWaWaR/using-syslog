#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
import logging
import logging.config
import logging.handlers

import redis
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
from tornado.options import define, options


class MySysLogHandler(logging.handlers.SysLogHandler):

    defaults = {
        'format': '%(levelname)s - %(message)s',
        'level': 'DEBUG',
        'address': '/dev/log',
        'facility': 'local6',
        'ident': 'python',
    }

    def __init__(self, **kwargs):
        Cls = self.__class__
        kwargs.setdefault('address', Cls.defaults['address'])
        kwargs.setdefault('facility', Cls.defaults['facility'])
        ident = kwargs.pop('ident', Cls.defaults['ident'])
        super(MySysLogHandler, self).__init__(**kwargs)
        self.ident = ident

    def format(self, record):
        msg = super(MySysLogHandler, self).format(record)
        return u'{}[{}]: {}'.format(self.ident, record.process, msg)

    @classmethod
    def config_logging(Cls,
                       format=None,
                       level=None,
                       address=None,
                       facility=None,
                       ident=None):
        """
        [Reference]:
          https://docs.python.org/2/howto/logging-cookbook.html#configuring-filters-with-dictconfig
        """

        class_name = '{}.{}'.format(__name__, Cls.__name__)
        format = format or Cls.defaults['format']
        level = level or Cls.defaults['level']
        address = address or Cls.defaults['address']
        facility = facility or Cls.defaults['facility']
        ident = ident or Cls.defaults['ident']

        log_config = {
            'version': 1,
            'formatters': {
                'local': {
                    'format': format,
                }
            },
            'handlers': {
                'syslog': {
                    'class': class_name,
                    'formatter': 'local',
                    'address': address,
                    'facility': facility,
                    'ident': ident,
                },
            },
            'root': {
                'level': level,
                'handlers': ['syslog']
            },
        }
        logging.config.dictConfig(log_config)


MySysLogHandler.config_logging()
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
        #   RuntimeError: Cannot run in multiple processes:
        #    IOLoop instance has already been initialized.
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
