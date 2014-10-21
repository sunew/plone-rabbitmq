# -*- coding: utf-8 -*-

import time
import logging
import datetime

from email.Header import Header
from lxml import etree
from five import grok
from urllib2 import URLError

from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from ZODB.POSException import ConflictError

from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.interfaces import IProducer

from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.uuid.utils import uuidToObject
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode

SIMPLE_DEBUG = True



logger = logging.getLogger("rabbitmqtest")


def getView(context, request, name):
    # Remove the acquisition wrapper (prevent false context assumptions)
    context = aq_inner(context)
    # May raise ComponentLookUpError
    view = getMultiAdapter((context, request), name=name)
    # Add the view to the acquisition chain
    view = view.__of__(context)
    return view


class ITestMessage(Interface):
    """Marker interface."""

    def __init__(self, username, password, ean, **kwargs):
        self.__dict__.update(kwargs)


class TestProducer(Producer):
    grok.name("testrabbit.testqueue")

    connection_id = "testrabbit"
    exchange = "testrabbit"
    serializer = "application/x-python-serialize"

    auto_declare = True
    durable = True


class TestConsumer(Consumer):
    grok.name("testrabbit.testqueue")

    connection_id = "testrabbit"
    exchange = "testrabbit"
    serializer = "application/x-python-serialize"

    auto_declare = True
    durable = True

    marker = ITestMessage


@grok.subscribe(ITestMessage, IMessageArrivedEvent)
def processTestMessage(message, event):
    uuid = message.header_frame.correlation_id
    logger.info("Processing message: %s." % message.header_frame.message_id)

    # this is our obj:
    obj = uuidToObject(uuid)
    data = message.body

    if obj is None:
        logger.warn("Unable to find object (%s); rejecting." % uuid)
        message.reject(False)
        return

    site = getSite()
