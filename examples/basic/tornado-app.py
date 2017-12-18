#!/usr/bin/env python
# coding: utf-8

import logging
import logging.config
import logging.handlers

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info('get: Hello, world')
        self.write("Hello, world")


def make_app():
    log_config = {
        'version': 1,
        'formatters': {
            'local': {
                'format': '%(asctime)s %(message)s',
            }
        },
        'handlers': {
            'syslog': {
                'class': 'logging.handlers.SysLogHandler',
                'facility': 'local6',
                'address': '/dev/log',
                'formatter': 'local',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['syslog']
        },
    }
    logging.config.dictConfig(log_config)

    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8877)
    tornado.ioloop.IOLoop.current().start()
