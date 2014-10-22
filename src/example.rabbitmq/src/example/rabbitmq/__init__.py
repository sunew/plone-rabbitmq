# -*- extra stuff goes here -*-
import os
import logging
import pika.log

from zope.i18nmessageid import MessageFactory
import rabbitmq

rabbitmqMessageFactory = MessageFactory('example.rabbitmq')

pikalog = logging.getLogger('pika')

pika_log_level = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
}.get(os.environ.get('PIKA_LOGLEVEL'), logging.INFO)

if pika_log_level == logging.DEBUG:
    pika.log.debug = logging.info

pikalog.setLevel(pika_log_level)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
