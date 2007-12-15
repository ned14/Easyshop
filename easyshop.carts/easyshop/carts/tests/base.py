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

import easyshop.carts
from plone.app import relations

setupCoreSessions()
ZopeTestCase.installProduct('SiteAccess') 

ZopeTestCase.installProduct("EasyShop", "plone.app.relations")
PloneTestCase.setupPloneSite(products=['EasyShop', "plone.app.relations"])

class EasyShopCartsSite(PloneSite):

    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        # login as admin (copied from `loginAsPortalOwner`)
        uf = app.acl_users
        user = uf.getUserById(PloneTestCase.portal_owner).__of__(uf)
        newSecurityManager(None, user)
        zcml.load_config('configure.zcml', easyshop.carts)
        zcml.load_config('configure.zcml', relations)        

        portal.invokeFactory("EasyShop", 'shop', title="EasyShop")
        portal.portal_workflow.doActionFor(portal.shop, "publish")
        portal.shop.at_post_create_script()
        
        portal.shop.products.invokeFactory("Product", 'product', title="Product")
        portal.portal_workflow.doActionFor(portal.shop.products.product, "publish")

        portal.product = portal.shop.products.product
        
        commit()
        ZopeTestCase.close(app)

class EasyShopCartsTestCase(PloneTestCase.PloneTestCase):

    layer = EasyShopCartsSite

class EasyShopCartsFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    layer = EasyShopCartsSite
