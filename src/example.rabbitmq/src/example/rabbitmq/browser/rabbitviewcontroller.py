import time
import logging
from zope.interface import implements, Interface
from zope.component import getUtility

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID

from collective.zamqp.interfaces import IProducer

from example.rabbitmq import rabbitmqMessageFactory as _


class IRabbitController(Interface):
    """
    """

    def test():
        """ test method"""


class RabbitController(BrowserView):
    """
    """
    implements(IRabbitController)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        if self.request.form.has_key('test-rabbit'):
            # demo: using the session token as id:
            session_id = self.request.SESSION.token
            time_id = str(int(time.time()))
            message_id = "%s-%s" % (session_id, time_id)
            producer = getUtility(IProducer, name="testrabbit.testqueue")
            producer._register()

            message_data = {'key1': 'data1', 'key2': 'data2'}

            producer.publish(
                message_data, message_id=message_id,
                correlation_id=IUUID(self.context),
                )
            logging.info("Message sent: %s." % message_id)
            # process the request
            return 'OK'
        else:
            return 'Nothing in request'
