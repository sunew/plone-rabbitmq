# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

import rabbitmq

rabbitmqMessageFactory = MessageFactory('example.rabbitmq')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
