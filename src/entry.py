# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

# -- stdlib --
import argparse
import datetime
import logging
import sys

# -- third party --
from bottle import run
from raven.handlers.logging import SentryHandler
from raven.transport.gevent import GeventedHTTPTransport
import raven
import yaml

# -- own --
from state import State
from utils import spawn_autorestart
import main


# -- code --
def patch_gevent_hub_print_exception():
    from gevent.hub import Hub

    def print_exception(self, context, type, value, tb):
        import logging
        log = logging.getLogger('exception')
        log.error(
            '%s failed with %s',
            context, getattr(type, '__name__', 'exception'),
            exc_info=(type, value, tb),
        )

    Hub.print_exception = print_exception


def init_logging():
    root = logging.getLogger()
    root.setLevel(0)

    if State.config['sentry']:
        patch_gevent_hub_print_exception()
        hdlr = SentryHandler(raven.Client(State.config['sentry'], transport=GeventedHTTPTransport))
        hdlr.setLevel(logging.ERROR)
        root.addHandler(hdlr)

    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setLevel(getattr(logging, logging.DEBUG))

    root.addHandler(hdlr)

    root.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    root.info('==============================================')


def start():
    logging.basicConfig()

    parser = argparse.ArgumentParser('falcon-alarm')
    parser.add_argument('--config', help='Config file')
    parser.add_argument('--host', help='HTTP host', default='127.0.0.1')
    parser.add_argument('--port', help='HTTP port', default=6060)
    options = parser.parse_args()

    State.options = options
    State.alarms = {}
    State.config = yaml.load(open(options.config).read())

    import restapi  # noqa
    spawn_autorestart(main.process_events)

    run(server='gevent', host=options.host, port=options.port)


if __name__ == '__main__':
    start()
