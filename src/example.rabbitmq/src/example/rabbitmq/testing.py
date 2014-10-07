from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class ExamplerabbitmqLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import example.rabbitmq
        xmlconfig.file(
            'configure.zcml',
            example.rabbitmq,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.rabbitmq:default')

EXAMPLE_RABBITMQ_FIXTURE = ExamplerabbitmqLayer()
EXAMPLE_RABBITMQ_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_RABBITMQ_FIXTURE,),
    name="ExamplerabbitmqLayer:Integration"
)
EXAMPLE_RABBITMQ_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_RABBITMQ_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ExamplerabbitmqLayer:Functional"
)
