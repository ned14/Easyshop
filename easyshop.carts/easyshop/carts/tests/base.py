# Suppress DeprecationWarnings, we really don't want any in these tests
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)

from AccessControl.SecurityManagement import newSecurityManager
from transaction import commit
from Products.Five import zcml
from Testing import ZopeTestCase
from Testing.ZopeTestCase.utils import setupCoreSessions
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite

import easyhop.carts

setupCoreSessions()
ZopeTestCase.installProduct('SiteAccess') 
PloneTestCase.setupPloneSite()

class EasyShopCartsSite(PloneSite):

    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        # login as admin (copied from `loginAsPortalOwner`)
        uf = app.acl_users
        user = uf.getUserById(PloneTestCase.portal_owner).__of__(uf)
        newSecurityManager(None, user)
        zcml.load_config('configure.zcml', easyhop.carts)

        portal.invokeFactory("Document", 'document', title="Document")
        portal.portal_workflow.doActionFor(portal.document, "publish")
        
        commit()
        ZopeTestCase.close(app)


class EasyShopCartsTestCase(PloneTestCase.PloneTestCase):

    layer = EasyShopCartsSite

class EasyShopCartsFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    layer = EasyShopCartsSite
