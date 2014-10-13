from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from example.rabbitmq import rabbitmqMessageFactory as _


class IRabbitViewView(Interface):
    """
    RabbitView view interface
    """

    def test():
        """ test method"""


class RabbitViewView(BrowserView):
    """
    RabbitView browser view
    """
    implements(IRabbitViewView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}
